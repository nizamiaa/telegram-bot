from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
import yt_dlp
import os

TOKEN = os.getenv("TOKEN")


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salam 👋\n\nMənə TikTok, Instagram və ya YouTube linki göndər 🙂"
    )


# main handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not url.startswith("http"):
        await update.message.reply_text("❌ Zəhmət olmasa düzgün link göndər")
        return

    await update.message.reply_text("⏳ Video yüklənir...")

    ydl_opts = {
        "outtmpl": "video.%(ext)s",
        "format": "bv*+ba/best/best[ext=mp4]",
        "noplaylist": True,
        "quiet": True,
        # əgər cookies işlətmək istəyirsənsə aç:
        # "cookiefile": "cookies.txt",
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=True)

        # faylı tap
        filename = None
        for f in os.listdir():
            if f.startswith("video"):
                filename = f
                break

        if not filename:
            await update.message.reply_text("❌ Video tapılmadı (private və ya login tələb edir)")
            return

        # video göndər (əgər böyükdürsə document kimi göndər)
        with open(filename, "rb") as video:
            try:
                await update.message.reply_video(video=video)
            except:
                video.seek(0)
                await update.message.reply_document(document=video)

        os.remove(filename)

    except Exception as e:
        error_text = str(e)

        if "No video formats found" in error_text:
            await update.message.reply_text(
                "⚠️ Bu video private-dir və ya login tələb edir."
            )
        else:
            await update.message.reply_text(f"❌ Xəta: {error_text}")


# bot setup
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot işə düşdü...")
app.run_polling()

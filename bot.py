from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
import yt_dlp
import os

import os
TOKEN = os.getenv("TOKEN")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salam 👋\n\nMənə TikTok və ya Instagram video linki göndər 🙂"
    )

# main handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    # ❗ link yoxlaması
    if not url.startswith("http"):
        await update.message.reply_text("❌ Zəhmət olmasa düzgün link göndər")
        return

    await update.message.reply_text("⏳ Video yüklənir...")

    try:
        ydl_opts = {
    	"outtmpl": "video.%(ext)s",
    	"cookiefile": "cookies.txt",
    	"format": "best",
    	"noplaylist": True
	}

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # video göndər
        with open(filename, "rb") as video:
            await update.message.reply_video(video=video)

        # faylı sil
        os.remove(filename)

    except Exception as e:
        error_text = str(e)

        if "empty media response" in error_text:
            await update.message.reply_text(
                "⚠️ Bu video yalnız login ilə açılır və ya private-dir."
            )
        else:
            await update.message.reply_text(f"❌ Xəta: {error_text}")


# bot setup
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot işə düşdü...")
app.run_polling()

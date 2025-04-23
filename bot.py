import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import yt_dlp

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, _):
    await update.message.reply_text(
        "🔥 **24/7 Video Downloader**\n\n"
        "Kirim link:\n"
        "- YouTube\n- Instagram\n- Twitter/X\n- Facebook\n\n"
        "Contoh: https://youtu.be/xxxx"
    )


async def download(update: Update, _):
    url = update.message.text
    user = update.message.from_user

    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await update.message.reply_video(
            video=open(filename, 'rb'),
            caption=f"🎬 {info['title']}"
        )
        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


if __name__ == '__main__':
    TOKEN = os.getenv("BOT_TOKEN")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

    app.run_polling()

import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import yt_dlp

# 🔑 Apni real details yahan " " ke andar dalein
BOT_TOKEN = "8653934041:AAGEN4AcrPTAW0dZUcW9EgIUKPaKw1dZErw"
SPONSOR_CHANNEL = "@FastVideoDownlooader_bot"
SHORTENER_API_KEY = "f31e49330a7c005bfe7d38abc1d76b1b67a57093"

def shorten_url(long_url):
    api_url = f"https://gplinks.in{SHORTENER_API_KEY}&url={long_url}"
    try:
        response = requests.get(api_url).json()
        if response.get("status") == "success":
            return response.get("shortenedUrl")
    except Exception:
        pass
    return long_url

def is_subscribed(bot, user_id):
    try:
        member = bot.get_chat_member(chat_id=SPONSOR_CHANNEL, user_id=user_id)
        if member.status in ['member', 'creator', 'administrator']:
            return True
    except Exception:
        return False
    return False

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("👋 Welcome! Mujhe kisi bhi video ka link bhejein, main download link bana kar dunga.")

def handle_video_link(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    url = update.message.text

    if not is_subscribed(context.bot, user_id):
        keyboard = [
            [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me{SPONSOR_CHANNEL.strip('@')}")],
            [InlineKeyboardButton("✅ I Have Joined", callback_data="check_join")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("⚠️ Bot use karne ke liye aapko hamare sponsor channel ko join karna hoga!", reply_markup=reply_markup)
        return

    update.message.reply_text("⏳ Video link extract ho raha hai, kripya intezar karein...")

    ydl_opts = {'format': 'best'}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url', None)
            title = info.get('title', 'Video')

        if video_url:
            ad_link = shorten_url(video_url)
            keyboard = [[InlineKeyboardButton("📥 Download Video (Watch Ad)", url=ad_link)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(f"🎬 **Title:** {title}\n\nButton par click karein aur ad dekh kar video download karein!", reply_markup=reply_markup, parse_mode="Markdown")
        else:
            update.message.reply_text("❌ Is link se video download nahi ho sapti.")
    except Exception:
        update.message.reply_text("❌ Sahi link bhejein ya thodi der baad try karein.")

def main():
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_video_link))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

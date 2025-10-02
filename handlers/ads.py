from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler
from models import access
import datetime

def ads_menu(update: Update, context: CallbackContext):
    user = update.effective_user
    if access.has_access(user.id):
        tl = access.time_left(user.id)
        hrs = round(tl.total_seconds() / 3600, 1)
        update.message.reply_text(
            f"✅ You already have access!\n⏳ Time left: {hrs} hours"
        )
    else:
        keyboard = [[InlineKeyboardButton("▶️ Watch Ad", callback_data="watchad")]]
        update.message.reply_text(
            "⚡ Watch an ad to unlock 12 hours of lecture access:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

def watch_ad(update: Update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user
    query.answer()

    # Here you can integrate real Ads API (Google/Custom)
    # For demo: simulate watching ad
    expiry = access.give_access(user.id, 12)
    query.edit_message_text(
        f"🎉 Ad watched successfully!\n"
        f"📚 You now have access for 12 hours (until {expiry})."
    )

# Register handlers
def register(dp):
    dp.add_handler(CallbackQueryHandler(watch_ad, pattern=r"^watchad$"))


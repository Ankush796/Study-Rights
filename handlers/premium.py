from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler
from models import premium

def premium_menu(update: Update, context: CallbackContext):
    user = update.effective_user
    if premium.has_premium(user.id):
        expiry = premium.get_premium_expiry(user.id)
        if expiry:
            update.message.reply_text(f"🌟 You are Premium!\n⏳ Valid till: {expiry}")
        else:
            update.message.reply_text("🌟 You have Lifetime Premium!")
        return

    keyboard = [
        [InlineKeyboardButton("1 Month - ₹99", callback_data="buy:30")],
        [InlineKeyboardButton("3 Months - ₹199", callback_data="buy:90")],
        [InlineKeyboardButton("Lifetime - ₹999", callback_data="buy:lifetime")]
    ]
    update.message.reply_text(
        "💎 Premium Plans:\n\n"
        "✨ Unlimited access to all lectures\n"
        "✨ No Ads\n"
        "✨ Special premium badge (coming soon)\n\n"
        "Choose a plan:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def buy_premium(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data.split(":")[1]
    user = query.from_user

    if data == "6 Months":
        premium.give_premium(user.id, None)
        query.edit_message_text("🎉 You are now 6 Months Premium!")
    else:
        days = int(data)
        expiry = premium.give_premium(user.id, days)
        query.edit_message_text(f"🎉 Premium activated for {days} days (till {expiry}).")

def register(dp):
    dp.add_handler(CallbackQueryHandler(buy_premium, pattern=r"^buy:"))


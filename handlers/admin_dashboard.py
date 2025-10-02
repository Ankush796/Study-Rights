from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler, MessageHandler, Filters
from models import user, premium, referral, access
import os

ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "0").split(",")))
broadcast_mode = {}

def admin_dashboard(update: Update, context: CallbackContext):
    if update.effective_user.id not in ADMIN_IDS:
        update.message.reply_text("🚫 You are not an admin.")
        return
    
    total_users = user.get_total_users()
    stats = (
        f"📊 *Admin Dashboard*\n\n"
        f"👥 Total Users: {total_users}\n"
        f"💎 Premium Users: {premium_count()}\n"
        f"🎯 Referrals Tracked: {total_referrals()}\n"
    )
    keyboard = [
        [InlineKeyboardButton("📢 Broadcast", callback_data="admin:broadcast")],
        [InlineKeyboardButton("👥 User List", callback_data="admin:users")]
    ]
    update.message.reply_text(stats, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

def premium_count():
    from pymongo import MongoClient
    client = MongoClient(os.getenv("MONGO_URI"))
    return client["ca_foundation"]["premium"].count_documents({"active": True})

def total_referrals():
    from pymongo import MongoClient
    client = MongoClient(os.getenv("MONGO_URI"))
    return client["ca_foundation"]["referrals"].count_documents({})

def admin_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data == "admin:broadcast":
        broadcast_mode[query.from_user.id] = True
        query.edit_message_text("✍️ Send me the broadcast message now:")
    elif query.data == "admin:users":
        users = user.get_all_users()
        msg = "👥 *User List:*\n\n"
        for u in users.limit(10):  # show first 10
            msg += f"🔹 {u.get('first_name')} (@{u.get('username')})\n"
        query.edit_message_text(msg, parse_mode="Markdown")

def broadcast_message(update: Update, context: CallbackContext):
    if update.effective_user.id in broadcast_mode and broadcast_mode[update.effective_user.id]:
        msg = update.message.text
        count = 0
        for u in user.get_all_users():
            try:
                context.bot.send_message(u["user_id"], msg)
                count += 1
            except:
                pass
        update.message.reply_text(f"✅ Broadcast sent to {count} users.")
        broadcast_mode[update.effective_user.id] = False

def register(dp):
    dp.add_handler(CallbackQueryHandler(admin_callback, pattern=r"^admin:"))
    dp.add_handler(MessageHandler(Filters.text & Filters.user(ADMIN_IDS), broadcast_message))

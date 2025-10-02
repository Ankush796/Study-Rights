 from telegram import Update
from telegram.ext import CallbackContext
from models.user import create_user, get_user
from datetime import datetime

def start(update: Update, context: CallbackContext):
    user = update.effective_user
    create_user(user.id, user.first_name)
    update.message.reply_text(
        f"👋 Hi {user.first_name}!\nWelcome to Study Rights 📚\n\n"
        "👉 Use /menu to explore lectures"
    )

def menu(update: Update, context: CallbackContext):
    update.message.reply_text(
        "📚 Main Menu\n"
        "1️⃣ Subjects\n"
        "2️⃣ Ads Access\n"
        "3️⃣ Premium Plans\n"
        "4️⃣ Referral Rewards\n"
        "5️⃣ /profile (Check your account)"
    )

def profile(update: Update, context: CallbackContext):
    user = get_user(update.effective_user.id)
    if user:
        expiry = user['access_until'].strftime("%Y-%m-%d %H:%M")
        premium = "✅ Premium" if user.get("premium") else "❌ Free"
        update.message.reply_text(
            f"👤 Profile:\n\n"
            f"Name: {user['name']}\n"
            f"UserID: {user['user_id']}\n"
            f"Access Until: {expiry}\n"
            f"Status: {premium}\n"
            f"Referrals: {user['referrals']}\n"
            f"Ads Watched: {user['ads_watched']}"
        )
    else:
        update.message.reply_text("⚠️ User not found. Try /start again.")
       

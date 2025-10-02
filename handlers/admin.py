from telegram import Update
from telegram.ext import CallbackContext
import os

ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "0").split(",")))

def admin_only(func):
    """Decorator to restrict admin commands"""
    def wrapper(update: Update, context: CallbackContext):
        if update.effective_user.id not in ADMIN_IDS:
            update.message.reply_text("🚫 You are not an admin.")
            return
        return func(update, context)
    return wrapper

@admin_only
def admin_panel(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🛠 Admin Panel\n"
        "- /addpremium <user_id> <months>\n"
        "- /broadcast <message>\n"
        "- (More coming soon...)"
    )


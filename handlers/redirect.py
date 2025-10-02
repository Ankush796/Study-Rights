from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

# Example: config me dusre bots
REDIRECT_BOTS = {
    "batchA": "https://t.me/CA_BatchA_Bot",
    "batchB": "https://t.me/CA_BatchB_Bot"
}

def redirect_menu(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📚 Batch A Bot", url=REDIRECT_BOTS["batchA"])],
        [InlineKeyboardButton("📚 Batch B Bot", url=REDIRECT_BOTS["batchB"])]
    ]
    update.message.reply_text("🔀 Choose a batch:", reply_markup=InlineKeyboardMarkup(keyboard))


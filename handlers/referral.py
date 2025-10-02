from telegram import Update
from telegram.ext import CallbackContext
from models import referral, access, premium

BOT_USERNAME = os.getenv("BOT_USERNAME", "CA_Foundation_Bot")

def my_referral(update: Update, context: CallbackContext):
    user = update.effective_user
    link = f"https://t.me/{BOT_USERNAME}?start={user.id}"
    count = referral.get_referrals(user.id)
    update.message.reply_text(
        f"👥 Invite your friends!\n\n"
        f"🔗 Your referral link:\n{link}\n\n"
        f"✅ You have referred {count} people."
    )

def start_with_referral(update: Update, context: CallbackContext):
    user = update.effective_user
    args = context.args
    if args:
        try:
            referrer_id = int(args[0])
            if referral.set_referrer(user.id, referrer_id):
                # Reward system: give 24h access or 3 days premium to referrer
                premium.give_premium(referrer_id, 3)  
                update.message.reply_text("🎉 Thanks for joining via referral!")
        except:
            pass


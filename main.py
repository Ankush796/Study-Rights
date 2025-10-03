
---

### 📄 main.py
```python
import os
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TG_BOT_TOKEN")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "0").split(",")))

# ---- Commands ----
def start(update, context):
    user = update.effective_user
    update.message.reply_text(
        f"👋 Hi {user.first_name}!\n\n"
        "Welcome to **Study Rights** 📚\n\n"
        "Use /menu to explore lectures."
    )

def menu(update, context):
    update.message.reply_text(
        "📚 Main Menu\n\n"
        "1. Subjects\n"
        "2. Ads Access\n"
        "3. Premium Plans\n"
        "4. Referral Rewards\n\n"
        "👉 Select option from buttons (coming soon)."
    )

# ---- Main ----
def main():
    if not TOKEN:
        print("❌ ERROR: TG_BOT_TOKEN not set in .env")
        return
    
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # Handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("menu", menu))

    print("✅ Bot is running...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
from jobs.expiry import start_scheduler
...
    # Start background jobs
    start_scheduler()
from handlers import user, admin, lectures
from telegram.ext import Updater, CommandHandler

...

    # User commands
    dp.add_handler(CommandHandler("start", user.start))
    dp.add_handler(CommandHandler("menu", user.menu))
    dp.add_handler(CommandHandler("profile", user.profile))
    dp.add_handler(CommandHandler("subjects", lectures.subjects))

    # Admin commands
    dp.add_handler(CommandHandler("admin", admin.admin_panel))
    dp.add_handler(CommandHandler("addsubject", admin.add_subject))
    dp.add_handler(CommandHandler("addfaculty", admin.add_faculty))
    dp.add_handler(CommandHandler("addchapter", admin.add_chapter))

    # Callback queries
    lectures.register(dp)
from handlers import premium

    # Premium
    dp.add_handler(CommandHandler("premium", premium.premium_menu))
    premium.register(dp)
from handlers import referral

def start(update, context):
    user = update.effective_user
    args = context.args
    if args:
        referral.start_with_referral(update, context)
    update.message.reply_text(
        f"👋 Hi {user.first_name}!\n"
        "Welcome to **Study Rights** 📚\n\n"
        "Use /menu to explore lectures.\n"
        "Use /referral to invite friends."
    )

    # save user to DB if not exists (optional)
    

    # Handlers
    dp.add_handler(CommandHandler("referral", referral.my_referral))
from handlers import admin_dashboard
from models import user

def start(update, context):
    u = update.effective_user
    user.save_user(u)   # save new user
    ...
    
    dp.add_handler(CommandHandler("admindash", admin_dashboard.admin_dashboard))
    admin_dashboard.register(dp)
from jobs.scheduler import start_scheduler
from handlers import redirect

def main():
    ...
    # Start scheduler
    start_scheduler()

    # Redirect command
    dp.add_handler(CommandHandler("redirect", redirect.redirect_menu))
from config import BOT_TOKEN, ADMINS, REDIRECT_BOT, LOG_GROUP, MONGO_URI, BOT_USERNAME, DEFAULT_LANG

# Example use
print(f"✅ Bot {BOT_USERNAME} started with default lang: {DEFAULT_LANG}")


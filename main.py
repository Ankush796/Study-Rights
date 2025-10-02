
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


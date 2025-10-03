import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TG_BOT_TOKEN")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "0").split(",")))

# ====== Handlers Imports ======
from jobs.scheduler import start_scheduler   # ✅ only scheduler.py, expiry.py removed
from handlers import user, admin, lectures, premium, referral, admin_dashboard, redirect
from models import user as user_model
from config import BOT_TOKEN, ADMINS, REDIRECT_BOT, LOG_GROUP, MONGO_URI, BOT_USERNAME, DEFAULT_LANG


# ---- Simple Commands ----
async def start(update, context):
    u = update.effective_user
    args = context.args

    # Referral support
    if args:
        await referral.start_with_referral(update, context)

    # Save user to DB
    try:
        user_model.save_user(u)
    except Exception as e:
        print(f"User save error: {e}")

    await update.message.reply_text(
        f"👋 Hi {u.first_name}!\n"
        "Welcome to **Study Rights** 📚\n\n"
        "Use /menu to explore lectures.\n"
        "Use /referral to invite friends."
    )


async def menu(update, context):
    await update.message.reply_text(
        "📚 Main Menu\n\n"
        "1. Subjects\n"
        "2. Ads Access\n"
        "3. Premium Plans\n"
        "4. Referral Rewards\n\n"
        "👉 Select option from buttons (coming soon)."
    )


# ---- Main Function ----
def main():
    if not TOKEN:
        print("❌ ERROR: TG_BOT_TOKEN not set in .env")
        return

    app = Application.builder().token(BOT_TOKEN).build()

    # === User commands ===
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("profile", user.profile))
    app.add_handler(CommandHandler("subjects", lectures.subjects))
    app.add_handler(CommandHandler("referral", referral.my_referral))
    app.add_handler(CommandHandler("premium", premium.premium_menu))
    app.add_handler(CommandHandler("redirect", redirect.redirect_menu))

    # === Admin commands ===
    app.add_handler(CommandHandler("admin", admin.admin_panel))
    app.add_handler(CommandHandler("addsubject", admin.add_subject))
    app.add_handler(CommandHandler("addfaculty", admin.add_faculty))
    app.add_handler(CommandHandler("addchapter", admin.add_chapter))
    app.add_handler(CommandHandler("admindash", admin_dashboard.admin_dashboard))

    # === Register callbacks ===
    lectures.register(app)
    premium.register(app)
    referral.register(app)
    admin_dashboard.register(app)

    # === Background Jobs ===
    try:
        start_scheduler()
    except Exception as e:
        print(f"Scheduler error: {e}")

    print(f"✅ Bot {BOT_USERNAME} started with default lang: {DEFAULT_LANG}")
    app.run_polling()


if __name__ == "__main__":
    main()

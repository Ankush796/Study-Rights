import os
from telegram import Update
from telegram.ext import CallbackContext
from models import lecture

# ✅ Admins from ENV
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "0").split(",")))


# ✅ Decorator for admin-only commands
def admin_only(func):
    def wrapper(update: Update, context: CallbackContext):
        if update.effective_user.id not in ADMIN_IDS:
            update.message.reply_text("🚫 You are not an admin.")
            return
        return func(update, context)
    return wrapper


# ✅ Admin Panel Command (merged both versions)
@admin_only
def admin_panel(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🛠 Admin Panel\n\n"
        "➡️ General Commands:\n"
        "- /addpremium <user_id> <months>\n"
        "- /broadcast <message>\n\n"
        "➡️ Lecture Management:\n"
        "- /addsubject <subject>\n"
        "- /addfaculty <subject> <faculty>\n"
        "- /addchapter <subject> <faculty> <chapter> <link>\n"
    )


# ✅ Add Subject
@admin_only
def add_subject(update: Update, context: CallbackContext):
    if len(context.args) < 1:
        update.message.reply_text("⚠️ Usage: /addsubject <subject>")
        return
    subject = " ".join(context.args)
    lecture.add_subject(subject)
    update.message.reply_text(f"✅ Subject added: {subject}")


# ✅ Add Faculty
@admin_only
def add_faculty(update: Update, context: CallbackContext):
    if len(context.args) < 2:
        update.message.reply_text("⚠️ Usage: /addfaculty <subject> <faculty>")
        return
    subject, faculty = context.args[0], " ".join(context.args[1:])
    lecture.add_faculty(subject, faculty)
    update.message.reply_text(f"✅ Faculty '{faculty}' added to subject '{subject}'")


# ✅ Add Chapter
@admin_only
def add_chapter(update: Update, context: CallbackContext):
    if len(context.args) < 4:
        update.message.reply_text(
            "⚠️ Usage: /addchapter <subject> <faculty> <chapter> <link>"
        )
        return
    subject, faculty, chapter, link = (
        context.args[0],
        context.args[1],
        context.args[2],
        context.args[3],
    )
    lecture.add_chapter(subject, faculty, chapter, link)
    update.message.reply_text(f"✅ Chapter '{chapter}' added under {subject}/{faculty}")

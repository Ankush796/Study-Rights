from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler
from models import lecture, access


# ✅ Subjects Menu
def subjects(update: Update, context: CallbackContext):
    user = update.effective_user

    # Access check (Ad Access / Premium)
    if not access.has_full_access(user.id):
        update.message.reply_text("🚫 Please watch an ad (/ads) or buy premium (/premium).")
        return

    subjects = lecture.get_subjects()
    if not subjects:
        update.message.reply_text("⚠️ No subjects available yet.")
        return

    keyboard = [[InlineKeyboardButton(s, callback_data=f"subject:{s}")] for s in subjects]
    update.message.reply_text("📚 Choose a subject:", reply_markup=InlineKeyboardMarkup(keyboard))


# ✅ Faculties Menu
def faculties(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    subject = query.data.split(":")[1]
    faculties = lecture.get_faculties(subject)

    if not faculties:
        query.edit_message_text(f"⚠️ No faculties found for {subject}.")
        return

    keyboard = [[InlineKeyboardButton(f, callback_data=f"faculty:{subject}:{f}")] for f in faculties]
    query.edit_message_text(f"👨‍🏫 Faculties for {subject}:", reply_markup=InlineKeyboardMarkup(keyboard))


# ✅ Chapters Menu
def chapters(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    _, subject, faculty = query.data.split(":")
    chapters = lecture.get_chapters(subject, faculty)

    if not chapters:
        query.edit_message_text(f"⚠️ No chapters found for {faculty} in {subject}.")
        return

    keyboard = [[InlineKeyboardButton(c["name"], url=c["link"])] for c in chapters]
    query.edit_message_text(f"📖 Chapters by {faculty}:", reply_markup=InlineKeyboardMarkup(keyboard))


# ✅ Register Handlers
def register(dp):
    dp.add_handler(CallbackQueryHandler(faculties, pattern=r"^subject:"))
    dp.add_handler(CallbackQueryHandler(chapters, pattern=r"^faculty:"))

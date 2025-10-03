from telegram import Update
from telegram.ext import CallbackContext
from datetime import datetime

from models.user import create_user, get_user
from models import premium
from handlers.ui import home_keyboard, t

# === Start Command ===

def start(update: Update, context: CallbackContext):
user = update.effective_user
create_user(user.id, user.first_name)

```
update.message.reply_text(
    t("welcome", name=user.first_name),
    reply_markup=home_keyboard(),
    parse_mode="Markdown"
)
```

# === Menu Command ===

def menu(update: Update, context: CallbackContext):
update.message.reply_text(
t("menu_title"),
reply_markup=home_keyboard(),
parse_mode="Markdown"
)

# === Profile Command ===

def profile(update: Update, context: CallbackContext):
u = get_user(update.effective_user.id)

```
if u:
    expiry = (
        u["access_until"].strftime("%Y-%m-%d %H:%M")
        if u.get("access_until")
        else "N/A"
    )
    badge = "💎 Premium" if premium.has_premium(u["user_id"]) else "🆓 Free User"

    update.message.reply_text(
        f"👤 *Profile*\n\n"
        f"Name: {u.get('name')}\n"
        f"UserID: {u.get('user_id')}\n"
        f"Access Until: {expiry}\n"
        f"Status: {badge}\n"
        f"Referrals: {u.get('referrals', 0)}\n"
        f"Ads Watched: {u.get('ads_watched', 0)}",
        parse_mode="Markdown"
    )
else:
    update.message.reply_text("⚠️ User not found. Try /start again.")
```

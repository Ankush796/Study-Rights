from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def home_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 Subjects", callback_data="menu:subjects")],
        [InlineKeyboardButton("▶️ Watch Ads", callback_data="menu:ads")],
        [InlineKeyboardButton("💎 Premium", callback_data="menu:premium")],
        [InlineKeyboardButton("👥 Referral", callback_data="menu:referral")],
        [InlineKeyboardButton("ℹ️ Profile", callback_data="menu:profile")]
    ])

def back_home():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Home", callback_data="menu:home")]])
import json, os

LANG = os.getenv("DEFAULT_LANG", "en")
with open(f"locales/{LANG}.json", "r", encoding="utf-8") as f:
    TEXTS = json.load(f)

def t(key, **kwargs):
    return TEXTS[key].format(**kwargs)


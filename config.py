import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Telegram Bot
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")

# Database
MONGO_URI = os.getenv("MONGO_URI")

# Settings
DEFAULT_LANG = os.getenv("DEFAULT_LANG", "en")

# Admins (comma separated IDs)
ADMINS = [int(x) for x in os.getenv("ADMINS", "").split(",") if x]

# Redirect bot (expired content/multi-bot system)
REDIRECT_BOT = os.getenv("REDIRECT_BOT")

# Log group (optional, for errors/logs)
LOG_GROUP = int(os.getenv("LOG_GROUP", "0"))

# Check if critical values are missing
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN is missing in .env")

if not MONGO_URI:
    raise ValueError("❌ MONGO_URI is missing in .env")

```python
from datetime import datetime, timedelta
from pymongo import MongoClient
import os

# === MongoDB Connection ===
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["Study_Rights"]   # ✅ database name fixed (avoid spaces)
users = db["users"]


# === Core User Functions ===
def get_user(user_id: int):
    """Fetch user by Telegram ID."""
    return users.find_one({"user_id": user_id})


def create_user(user_id: int, name: str):
    """Create a new user if not exists."""
    if not get_user(user_id):
        users.insert_one({
            "user_id": user_id,
            "name": name,
            "joined_at": datetime.utcnow(),
            "access_until": datetime.utcnow(),   # Default no extra access
            "premium": False,
            "referrals": 0,
            "ads_watched": 0
        })


def save_user(user):
    """Save or update Telegram user info."""
    users.update_one(
        {"user_id": user.id},
        {
            "$set": {
                "first_name": user.first_name,
                "username": user.username,
                "joined": datetime.utcnow()
            }
        },
        upsert=True
    )


def add_access(user_id: int, hours: int):
    """Add hours of free access (ads/referrals)."""
    user = get_user(user_id)
    if user:
        current_expiry = user.get("access_until", datetime.utcnow())
        if current_expiry < datetime.utcnow():
            current_expiry = datetime.utcnow()
        new_expiry = current_expiry + timedelta(hours=hours)

        users.update_one(
            {"user_id": user_id},
            {"$set": {"access_until": new_expiry}}
        )
        return new_expiry
    return None


def set_premium(user_id: int, months: int = 1):
    """Upgrade to premium for given months."""
    user = get_user(user_id)
    if user:
        new_expiry = datetime.utcnow() + timedelta(days=30 * months)
        users.update_one(
            {"user_id": user_id},
            {"$set": {"premium": True, "access_until": new_expiry}}
        )
        return new_expiry
    return None


def has_premium(user_id: int) -> bool:
    """Check if user has premium access."""
    user = get_user(user_id)
    return bool(user and user.get("premium") and user.get("access_until") > datetime.utcnow())
```

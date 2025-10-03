```python
from pymongo import MongoClient
import os
import datetime

# === MongoDB Setup ===
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["ca_foundation"]
premium = db["premium"]


def give_premium(user_id: int, days: int = None):
    """
    Give premium access to a user.
    - If `days` is provided, expiry = now + days
    - If `days` is None, user gets lifetime premium
    """
    expiry = datetime.datetime.utcnow() + datetime.timedelta(days=days) if days else None
    premium.update_one(
        {"user_id": user_id},
        {"$set": {"expiry": expiry, "active": True}},
        upsert=True
    )
    return expiry


def has_premium(user_id: int) -> bool:
    """
    Check if user currently has active premium.
    Returns:
        True  -> if lifetime or expiry date is still valid
        False -> if not premium or expired
    """
    record = premium.find_one({"user_id": user_id})
    if not record:
        return False

    expiry = record.get("expiry")  # safe lookup
    if expiry is None:  # Lifetime premium
        return True

    return expiry > datetime.datetime.utcnow()


def get_premium_expiry(user_id: int):
    """
    Get the expiry date of user's premium.
    Returns None if no premium or lifetime.
    """
    record = premium.find_one({"user_id": user_id})
    return record.get("expiry") if record else None
```

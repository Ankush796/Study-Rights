```python
from pymongo import MongoClient
import os

# === MongoDB Setup ===
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["ca_foundation"]
referrals = db["referrals"]


def set_referrer(new_user_id: int, referrer_id: int) -> bool:
    """
    Assign a referrer to a new user.
    Returns False if:
      - User tries to refer themselves
      - User already has a referrer
    """
    if new_user_id == referrer_id:
        return False

    if referrals.find_one({"user_id": new_user_id}):
        return False  # already referred before

    referrals.insert_one({
        "user_id": new_user_id,
        "referrer": referrer_id
    })
    return True


def get_referrer(user_id: int):
    """Return referrer ID of given user, or None if not referred."""
    record = referrals.find_one({"user_id": user_id})
    return record["referrer"] if record else None


def get_referrals(user_id: int) -> int:
    """Return number of referrals made by a given user."""
    return referrals.count_documents({"referrer": user_id})
```

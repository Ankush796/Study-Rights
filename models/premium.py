from pymongo import MongoClient
import os, datetime

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["ca_foundation"]
premium = db["premium"]

def give_premium(user_id: int, days: int = None):
    if days:
        expiry = datetime.datetime.utcnow() + datetime.timedelta(days=days)
    else:
        expiry = None  # Lifetime
    premium.update_one(
        {"user_id": user_id},
        {"$set": {"expiry": expiry, "active": True}},
        upsert=True
    )
    return expiry

def has_premium(user_id: int):
    record = premium.find_one({"user_id": user_id})
    if not record:
        return False
    if record["expiry"] is None:  # lifetime
        return True
    return record["expiry"] > datetime.datetime.utcnow()

def get_premium_expiry(user_id: int):
    record = premium.find_one({"user_id": user_id})
    if not record:
        return None
    return record["expiry"]


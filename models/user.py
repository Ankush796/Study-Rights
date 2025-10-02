from datetime import datetime, timedelta
from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["Study Rights"]
users = db["users"]

def get_user(user_id: int):
    return users.find_one({"user_id": user_id})

def create_user(user_id: int, name: str):
    if not get_user(user_id):
        users.insert_one({
            "user_id": user_id,
            "name": name,
            "joined_at": datetime.utcnow(),
            "access_until": datetime.utcnow(),   # free trial default: none
            "premium": False,
            "referrals": 0,
            "ads_watched": 0
        })

def add_access(user_id: int, hours: int):
    """Add hours of access for user (ads/referrals)."""
    user = get_user(user_id)
    if user:
        current_expiry = user["access_until"]
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
    """Upgrade to premium for X months."""
    user = get_user(user_id)
    if user:
        new_expiry = datetime.utcnow() + timedelta(days=30*months)
        users.update_one(
            {"user_id": user_id},
            {"$set": {"premium": True, "access_until": new_expiry}}
        )
        return new_expiry
    return None
from pymongo import MongoClient
import os, datetime

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["Study Rights"]
users = db["users"]

def save_user(user):
    users.update_one(
        {"user_id": user.id},
        {
            "$set": {
                "first_name": user.first_name,
                "username": user.username,
                "joined": datetime.datetime.utcnow()
            }
        },
        upsert=True
    )

def get_total_users():
    return users.count_documents({})

def get_all_users():
    return users.find()


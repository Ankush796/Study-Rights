from pymongo import MongoClient
import os, datetime

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["ca_foundation"]
access = db["access"]

def give_access(user_id: int, hours: int = 12):
    expiry = datetime.datetime.utcnow() + datetime.timedelta(hours=hours)
    access.update_one(
        {"user_id": user_id},
        {"$set": {"expiry": expiry}},
        upsert=True
    )
    return expiry

def has_access(user_id: int):
    record = access.find_one({"user_id": user_id})
    if not record:
        return False
    return record["expiry"] > datetime.datetime.utcnow()

def time_left(user_id: int):
    record = access.find_one({"user_id": user_id})
    if not record:
        return None
    return record["expiry"] - datetime.datetime.utcnow()


from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from pymongo import MongoClient
import os

# === MongoDB Setup ===
client = MongoClient(os.getenv("MONGO_URI"))
db = client["ca_foundation"]

users = db["users"]
access = db["access"]
premium = db["premium"]


# === Job 1: Check expired user access ===
def check_expired_access():
    now = datetime.utcnow()
    expired_users = users.find(
        {"access_until": {"$lt": now}, "premium": False}
    )

    for u in expired_users:
        # TODO: Later add Telegram notification here
        print(f"⚠️ User {u.get('user_id')} access expired.")


# === Job 2: Clean expired ads & premium ===
def clean_expired_access():
    now = datetime.utcnow()

    # Clean ads-based access
    access.delete_many({"expiry": {"$lte": now}})

    # Mark premium as inactive if expired
    premium.update_many(
        {"expiry": {"$lte": now}},
        {"$set": {"active": False}}
    )

    print("🧹 Cleaned expired access & premium")


# === Start Scheduler ===
def start_scheduler():
    scheduler = BackgroundScheduler()

    # Run jobs every 1 hour
    scheduler.add_job(check_expired_access, "interval", hours=1)
    scheduler.add_job(clean_expired_access, "interval", hours=1)

    scheduler.start()
    print("⏰ Expiry scheduler started")

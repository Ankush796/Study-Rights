from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from models.user import users

def check_expired_access():
    now = datetime.utcnow()
    expired_users = users.find({"access_until": {"$lt": now}, "premium": False})
    for u in expired_users:
        print(f"User {u['user_id']} access expired.")  # later -> send Telegram message

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_expired_access, 'interval', hours=1)
    scheduler.start()
from apscheduler.schedulers.background import BackgroundScheduler
from models import access, premium
import datetime

def clean_expired_access():
    from pymongo import MongoClient
    import os
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["ca_foundation"]

    now = datetime.datetime.utcnow()

    # Clean ads-based access
    db["access"].delete_many({"expiry": {"$lte": now}})
    
    # Clean expired premium
    db["premium"].update_many(
        {"expiry": {"$lte": now}}, 
        {"$set": {"active": False}}
    )

    print("🧹 Cleaned expired access & premium")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(clean_expired_access, "interval", hours=1)  # every 1 hr
    scheduler.start()


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


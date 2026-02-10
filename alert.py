import threading
import time
import schedule
from datetime import datetime, timedelta
from sqlalchemy import func
from database import SessionLocal
from models import User, Categories

def check_budget():
    with SessionLocal() as db:
        users = db.query(User).all()
        users_telegram_id = [user.budget for user in users if user.budget <= 1000]
        return users_telegram_id
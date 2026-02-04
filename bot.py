import telebot
from database import engine, SessionLocal


def get_db(): # enter to db
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


import telebot
from database import engine, SessionLocal, Base
from sqlalchemy.orm import Session
from data import bot_token
from models import User as UserModel

def get_db(): # enter to db
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)

bot = telebot.TeleBot(bot_token, parse_mode=None)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    telegram_id = message.from_user.id
    message_text = "Привет, для просмотра всех команд напишите команду /help"
    with SessionLocal() as db:
        if db.query(UserModel).filter(UserModel.telegram_id == telegram_id).first():
            bot.send_message(message.chat.id, message_text)
        else:
            new_user = UserModel(username=message.from_user.username, telegram_id=message.from_user.id) # create new user

            db.add(new_user)  # save user
            db.commit()
            db.refresh(new_user)

            bot.send_message(message.chat.id, message_text)


bot.infinity_polling()
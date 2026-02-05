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

@bot.message_handler(commands=['help'])
def help_info(message):
    bot.send_message(message.chat.id, "/start - запустить бота\n"
                                            "/help - показать список команд\n"
                                            "/add_balance Сумма - добавить сумму к текущему балансу\n"
                                            "/balance - текущий баланс"
                                                                                )


@bot.message_handler(commands=['add_balance'])
def add_balance(message):
    telegram_id = message.from_user.id
    money = message.text.split()[-1]

    for i in money:
        if i.isalpha():
            bot.send_message(message.chat.id, "Не правильный ввод, попробуйте сново")
            return

    with SessionLocal() as db:
        user = db.query(UserModel).filter(UserModel.telegram_id == telegram_id).first()
        if not user:
            bot.send_message(message.chat.id, "Сначало напишите команду /start")
            return
        if not user.current_balance:
            user.current_balance = int(money)
        else:
            user.current_balance += int(money)
        db.commit()
        db.refresh(user)
        bot.send_message(message.chat.id, f"Ваш баланс пополнен. Сейчас у вас {user.current_balance}")

@bot.message_handler(commands=['balance'])
def balance(message):
    telegram_id = message.from_user.id
    with SessionLocal() as db:
        user = db.query(UserModel).filter(UserModel.telegram_id == telegram_id).first()
        if not user:
            bot.send_message(message.chat.id, "Я вас не знаю, введите команду /start")
            return
        if user.current_balance is None:
            bot.send_message(message.chat.id, "Я не знаю ваш баланс, введите команду /add_balance")
            return
        bot.send_message(message.chat.id, f"Текущий баланс: {user.current_balance}")

@bot.message_handler(commands=['set_budget'])
def set_budget(message):
    telegram_id = message.from_user.id
    budget = message.text.split()[-1]

    for i in budget:
        if i.isalpha():
            bot.send_message(message.chat.id, "Я не знаю ваш месячный баланс, введите команду /add_balance")
            return

    with SessionLocal() as db:
        user = db.query(UserModel).filter(UserModel.telegram_id == telegram_id).first()
        if not user:
            bot.send_message(message.chat.id, "Я вас не знаю, введите команду /start")
        user.money_per_month = int(budget)
        db.commit()
        db.refresh(user)
        bot.send_message(message.chat.id, "Я сохранил ваш баланс.")





bot.infinity_polling(timeout=60, long_polling_timeout=60)
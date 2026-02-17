#standart
from datetime import date, datetime

#custom
import telebot
from sqlalchemy.sql import func

#project
from database import engine, SessionLocal, Base
from models import User as UserModel, Categories as CategoriesModel, Goals as GoalsModel
from data import bot_token
from functions import check_input


def get_db(): # enter to db
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)

bot = telebot.TeleBot(bot_token, parse_mode=None)

ALL_CATEGORY = {"жкх": "hcs", "еда": "food", "транспорт": "transport", "здоровье": "pharmacy", "кредит": "credits",
              "развлечения": "fun", "одежда": "cloth", "подушка": "financial_cushion", "цель": "target"}

# help text

HELP_TEXT = ("🤖 /start - запустить бота\n"
             "📖/help - показать список команд\n"
             "💰/add_balance Сумма - добавить сумму к текущему балансу\n"
             "💰/balance - текущий баланс\n"
             "💰/set_budget Сумма - сохранить ваш месячный доход\n"
             "💰/remove_balance Сумма - отнимает от вашего баланса сумму\n"
             "💰/expense Сумма Категория - сохраняет вашу трату\n"
             "💰/remove_expense dd-mm-yyyy Категория Сумма - удалит трату по указаным параметрам\n"
             "🎯/goal dd-mm-yyyy Цель Сумма - создаст цель для которой копите деньги\n"
             "📖/help_category - отобразит все категории\n")


HELP_CATEGORY_TEXT = ("🏠 ЖКХ\n🍔 Еда\n🚗 Транспорт\n💊 Здоровье"
                      "\n💳 Кредит\n🎭 Развлечения\n👕 Одежда\n💰 Подушка\n🎯 Цель")


# errors messages

NOT_FOUND_USER = "❌ Я вас не знаю, введите команду /start"
NOT_FOUND_CATEGORY = "❌ Такой категории нету"
NOT_FOUND_GOAL = "❌ Сначало вам нужно создать цель"
NOT_FOUND_EXPENSE = "❌ Такой траты нету"
INCORRECT_INPUT = "❌ Не правильный ввод, попробуйте сново"
BALANCE_LESS_THAN_ZERO = "❌ Ваш баланс не может быть меньше нуля"
BALANCE_IS_NONE = "❌ У вас не задан баланс"


# successful  messages

BALANCE_REPLENISHED = "✅ Ваш баланс пополнен"
BALANCE_REDUCED = "✅ Ваш баланс уменьшен"
MONTH_SAVE_BALANCE = "✅ Я сохранил ваш баланс. Если что-то измениться, напишите команду сново."
EXPENSE_SAVE = "✅ Трата сохранена"
EXPENSE_DELETE = "✅ Трата удалена"
GOAL_SAVE = "✅ Ваша цель записана, что-бы добавить бюджет к цели используйте команду /expense"




@bot.message_handler(commands=['start'])
async def send_welcome(message):
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
    bot.send_message(message.chat.id, HELP_TEXT)


@bot.message_handler(commands=['help_category'])
def help_category(message):
    bot.send_message(message.chat.id, HELP_CATEGORY_TEXT)



@bot.message_handler(commands=['add_balance'])
def add_balance(message):
    telegram_id = message.from_user.id
    money = message.text.split()[-1]


    if check_input(money) == 400:
        bot.send_message(message.chat.id, INCORRECT_INPUT)
        return


    with SessionLocal() as db:
        user = db.query(UserModel).filter(UserModel.telegram_id == telegram_id).first()


        if not user:
            bot.send_message(message.chat.id, NOT_FOUND_USER)
            return


        if not user.current_balance:
            user.current_balance = int(money)
        else:
            user.current_balance += int(money)


        db.commit()
        db.refresh(user)


    bot.send_message(message.chat.id, BALANCE_REPLENISHED)


@bot.message_handler(commands=['remove_balance'])
def remove_balance(message):
    telegram_id = message.from_user.id
    money = message.text.split()[-1]


    if check_input(money) == 400:
        bot.send_message(message.chat.id, INCORRECT_INPUT)
        return


    with SessionLocal() as db:
        user = db.query(UserModel).filter(UserModel.telegram_id == telegram_id).first()


        if not user:
            bot.send_message(message.chat.id, NOT_FOUND_USER)
            return


        if user.current_balance is None:
            bot.send_message(message.chat.id, BALANCE_IS_NONE)
            return


        if user.current_balance - int(money) < 0:
            bot.send_message(message.chat.id, BALANCE_LESS_THAN_ZERO)
            return


        user.current_balance -= int(money)
        db.commit()
        db.refresh(user)


    bot.send_message(message.chat.id, BALANCE_REDUCED)


@bot.message_handler(commands=['balance'])
def balance(message):
    telegram_id = message.from_user.id
    with SessionLocal() as db:
        user = (db.query(UserModel)
                .filter(UserModel.telegram_id == telegram_id)
                .first()
        )


        if not user:
            bot.send_message(message.chat.id, NOT_FOUND_USER)
            return


        if user.current_balance is None:
            bot.send_message(message.chat.id,
                        BALANCE_IS_NONE
            )
            return


    bot.send_message(message.chat.id,
                f"Текущий баланс: {user.current_balance}"
    )


@bot.message_handler(commands=['set_budget'])
def set_budget(message):
    telegram_id = message.from_user.id
    budget = message.text.split()[-1]


    if check_input(budget) == 400:
        bot.send_message(message.chat.id,
                    INCORRECT_INPUT
        )
        return


    with SessionLocal() as db:
        user = (db.query(UserModel)
                .filter(UserModel.telegram_id == telegram_id)
                .first()
        )


        if not user:
            bot.send_message(message.chat.id,
                        NOT_FOUND_USER
            )
            return


        user.money_per_month = int(budget)
        db.commit()
        db.refresh(user)


    bot.send_message(message.chat.id, )


@bot.message_handler(commands=['expense'])
def expense(message):
    if len(message.text.split()) <= 1:
        bot.send_message(message.chat.id,
                    INCORRECT_INPUT
        )
        return


    telegram_id = message.from_user.id
    money = message.text.split()[1]
    category = message.text.split()[-1]


    if check_input(money) == 400:
        bot.send_message(message.chat.id,
                    INCORRECT_INPUT
        )
        return


    if category.lower() not in ALL_CATEGORY:
        bot.send_message(message.chat.id, NOT_FOUND_CATEGORY)
        return


    col = ALL_CATEGORY[category.lower()]

    with SessionLocal() as db:
        user = (db.query(UserModel)
                .filter(UserModel.telegram_id == telegram_id)
                .first()
        )


        if not user:
            bot.send_message(message.chat.id,
                        NOT_FOUND_USER
            )
            return


        if user.current_balance is None:
            bot.send_message(message.chat.id, BALANCE_IS_NONE)
            return


        if user.current_balance - int(money) < 0:
            bot.send_message(message.chat.id,
                        BALANCE_LESS_THAN_ZERO
            )
            return


        if col == "target":
            goal_user = (db.query(GoalsModel)
                         .filter(user.id == GoalsModel.user_id)
                         .first()
            )


            if not goal_user:
                bot.send_message(message.chat.id,
                            NOT_FOUND_GOAL
                )
                return


            goal_user.currency_for_target += int(money)


        new_expense = CategoriesModel(user_id=user.id)
        setattr(new_expense, col, int(money))
        user.current_balance -= int(money)


        db.add(new_expense)
        db.commit()
        db.refresh(user)


    bot.send_message(message.chat.id, EXPENSE_SAVE)


@bot.message_handler(commands=['remove_expense'])
def remove_expense(message):
    telegram_id = message.from_user.id

    exp_date = message.text.split()[1]
    category = message.text.split()[2]
    money = message.text.split()[-1]

    year = exp_date.split("-")[-1]
    month = exp_date.split("-")[1]
    day = exp_date.split("-")[0]

    target_date = datetime(int(year), int(month), int(day)).date()


    if check_input(money) == 400:
        bot.send_message(message.chat.id,
                    INCORRECT_INPUT
        )
        return


    if category.lower() not in ALL_CATEGORY:
        bot.send_message(message.chat.id, NOT_FOUND_CATEGORY)
        return


    with SessionLocal() as db:
        user = (db.query(UserModel)
                .filter(UserModel.telegram_id == telegram_id)
                .first()
        )


        if not user:
            bot.send_message(message.chat.id, NOT_FOUND_USER)
            return


        expense = (db.query(CategoriesModel)
                   .filter(
                        CategoriesModel.user_id == user.id,
                        getattr(CategoriesModel, ALL_CATEGORY[category.lower()]) == int(money),
                        func.date(CategoriesModel.date) == target_date
                ).first()
        )


        if not expense:
            bot.send_message(message.chat.id, NOT_FOUND_EXPENSE)
            return


        user.current_balance += int(money)


        db.delete(expense)
        db.commit()
        db.refresh(user)


    bot.send_message(message.chat.id, EXPENSE_DELETE)


@bot.message_handler(commands=['expenses'])
def expenses(message):
    telegram_id = message.from_user.id
    with SessionLocal() as db:
        user = (db.query(UserModel)
                .filter(UserModel.telegram_id == telegram_id)
                .first()
        )


        expenses_db = (db.query(CategoriesModel)
                       .filter(CategoriesModel.user_id == user.id)
                       .all()
        )

        message_text = "---Категория---Сумма---Дата---\n"
        number = 1


        if not user:
            bot.send_message(message.chat.id,
                        NOT_FOUND_USER
            )
            return


        if not expenses_db:
            bot.send_message(message.chat.id, NOT_FOUND_EXPENSE)
            return


        for exp in expenses_db:
            for category in ALL_CATEGORY.values():
                amount = getattr(exp, category, 0)


                if amount > 0:
                    category_name = [x for x, j, in ALL_CATEGORY.items()
                                                    if j == category][0]

                    message_text += f"{number}. {category_name}: {amount}; {exp.date.strftime('%d-%m-%Y')}\n"
                    number += 1


    bot.send_message(message.chat.id, message_text)


@bot.message_handler(commands=['goal'])
def goal(message):
    telegram_id = message.from_user.id

    deadline_date = message.text.split()[1]
    target_name = message.text.split()[2]
    target_money = message.text.split()[-1]

    year = deadline_date.split("-")[-1]
    month = deadline_date.split("-")[1]
    day = deadline_date.split("-")[0]

    # format - deadline target_name target_money
    deadline=datetime(int(year), int(month), int(day))


    for i in target_money:
        if i.isalpha():
            bot.send_message(message.chat.id, INCORRECT_INPUT)
            return


    with SessionLocal() as db:
        user = (db.query(UserModel)
                .filter(UserModel.telegram_id == telegram_id)
                .first()
        )


        if not user:
            bot.send_message(message.chat.id, NOT_FOUND_USER)
            return


        new_goal = GoalsModel(user_id=user.id,
                              target=int(target_money),
                              target_name=target_name,
                              deadline=deadline
        )

        db.add(new_goal)
        db.commit()
        db.refresh(user)


    bot.send_message(message.chat.id, GOAL_SAVE)


@bot.message_handler(commands=['my_goals'])
def my_goals(message):
    telegram_id = message.from_user.id
    message_text = ""

    with SessionLocal() as db:
        user = (db.query(UserModel)
                .filter(UserModel.telegram_id == telegram_id)
                .first()
                )


        if not user:
            bot.send_message(message.chat.id, NOT_FOUND_USER)
            return

        goal_user = (db.query(GoalsModel)
                     .filter(user.id == GoalsModel.user_id)
                     .all()
        )

        for user_goal in goal_user:
            message_text += f"{user_goal.target_name}: {user_goal.currency_for_target}/{user_goal.target}\n"

        bot.send_message(message.chat.id, message_text)



bot.infinity_polling(timeout=5, long_polling_timeout = 1)
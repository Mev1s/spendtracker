from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, BigInteger, Float
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    telegram_id = Column(BigInteger, unique=True)
    money_per_month = Column(Integer, default=None)
    current_balance = Column(Integer, default=None)

class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    hcs = Column(Integer, default=0) # ЖКХ
    food = Column(Integer, default=0)
    transport = Column(Integer, default=0)
    pharmacy = Column(Integer, default=0)
    credits = Column(Integer, default=0)
    fun = Column(Integer, default=0)
    cloth = Column(Integer, default=0)
    financial_cushion = Column(Integer, default=0)
    target = Column(Integer, default=0)
    date = Column(DateTime, default=func.now())

class Goals(Base):
    __tablename__ = 'goals'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    target = Column(Integer, default=0)
    target_name = Column(String, default="")
    currency_for_target = Column(Integer, default=0)
    deadline = Column(DateTime, nullable=True)
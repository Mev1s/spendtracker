from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from data import password_base

SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{password_base}@localhost:5432/spendtracker"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# asyncio

ASYNC_DATABASE_URL = f"postgresql+asyncpg://postgres:{password_base}@localhost:5432/spendtracker"
async_engine = create_async_engine(ASYNC_DATABASE_URL)
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()
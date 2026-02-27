import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from main import app
from database import Base, get_db
from data import password_base

# Тестовая база данных PostgreSQL
TEST_DATABASE_URL = f"postgresql+asyncpg://postgres:{password_base}@localhost/test_spendtracker"


@pytest.fixture(scope="function")
async def engine():
    """Create test database engine."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine


@pytest.fixture(scope="function")
async def session(engine):
    """Create a fresh database session for each test."""
    async_session_maker = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session_maker() as session:
        # Начинаем транзакцию
        async with session:
            yield session


@pytest.fixture(scope="function")
async def client(session):
    """Create a test client with test database."""

    # Переопределяем зависимость get_db
    async def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()
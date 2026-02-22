import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.fixture
async def client():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
                     ) as client:
        yield client


async def test_get_users(client: AsyncClient):
    response = await client.get("/users")
    assert response.status_code == 200
    response = response.json()
    assert isinstance(response, list)
    for user in response:
        for key in ("id", "username", "telegram_id", "money_per_month", "current_balance"):
            assert key in user
            if key not in ("money_per_month", "current_balance"):
                assert user.get(key) is not None

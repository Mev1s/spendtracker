from httpx import AsyncClient, ASGITransport
from faker import Faker
import random
import datetime

fake = Faker()


# get tests

async def test_get_users(client: AsyncClient):
    response = await client.get("/users")
    assert response.status_code == 200
    response = response.json()
    assert isinstance(response, list)
    for user in response:
        for key in ("id",
                    "username",
                    "telegram_id",
                    "money_per_month",
                    "current_balance"
                ):
            assert key in user
            if key not in ("money_per_month", "current_balance"):
                assert user.get(key) is not None

async def test_get_users_by_id(client: AsyncClient):
    users = await client.get("/users")
    assert users.status_code == 200
    response = users.json()
    assert isinstance(response, list)
    for user in response:
        if "id" in user:
            response = await client.get(f"/users/{user["id"]}")
            assert response.status_code == 200
            response = response.json()
            assert isinstance(response, dict)


# post tests

async def test_post_user(client: AsyncClient):
    user_json = {"username": f"{fake.user_name()}",
                 "telegram_id": random.randint(1000*1000, 80*50000),
                 "money_per_month": random.randint(100, 10000),
                 "current_balance": random.randint(100, 1000000)
            }
    response = await client.post("/users", json=user_json)
    assert response.status_code == 200
    response = response.json()

    assert isinstance(response, dict)

    assert response["username"] == user_json["username"]
    assert response["telegram_id"] == user_json["telegram_id"]
    assert response["money_per_month"] == user_json["money_per_month"]
    assert response["current_balance"] == user_json["current_balance"]

async def test_post_goal_users(client: AsyncClient):
    users = await client.get("/users")
    users = users.json()
    for user in users:
        if "id" in user:
            goal_json = {"user_id": user["id"],
                         "target": random.randint(1000, 80*50000),
                         "target_name": fake.word(),
                         "currency_for_target": random.randint(100, 10000),
                         "deadline": str(fake.date_between(start_date='today', end_date='+1y'))
                    }
            response = await client.post("/goal", json=goal_json)
            assert response.status_code == 200
            response = response.json()

            assert isinstance(response, dict)

            assert response["user_id"] == goal_json["user_id"]
            assert response["target"] == goal_json["target"]
            assert response["target_name"] == goal_json["target_name"]
            assert response["currency_for_target"] == goal_json["currency_for_target"]
            assert response["deadline"][:10] == goal_json["deadline"][:10]


# delete tests


async def test_delete_goals(client: AsyncClient):
    goals = await client.get("/goals")
    goals = goals.json()
    for goal in goals:
        if "id" in goal:
            goal_id = goal["id"]
            response = await client.delete(f"/goal/delete/{goal_id}")
            assert response.status_code == 200

            response = response.json()
            assert isinstance(response, dict)
            assert response["id"] == goal_id
            assert response["target_name"] == goal["target_name"]
            assert response["target"] == goal["target"]
            assert response["currency_for_target"] == goal["currency_for_target"]
            assert response["deadline"][:10] == goal["deadline"][:10]


async def test_delete_user(client: AsyncClient):
    users = await client.get("/users")
    users = users.json()

    for user in users:
        if "id" in user:
            user_id = user["id"]
            response = await client.delete(f"/user/delete/{user_id}")
            assert response.status_code == 200
            response = response.json()
            assert isinstance(response, dict)

            assert response["id"] == user_id
            assert response["username"] == user["username"]
            assert response["telegram_id"] == user["telegram_id"]
            assert response["money_per_month"] == user["money_per_month"]
            assert response["current_balance"] == user["current_balance"]






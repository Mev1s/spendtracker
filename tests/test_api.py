from httpx import AsyncClient, ASGITransport
from faker import Faker
import random
import datetime
import pytest

fake = Faker()


# post tests

@pytest.mark.order(1)
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

@pytest.mark.order(2)
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


@pytest.mark.order(3)
async def test_post_categories(client: AsyncClient):
    response = await client.get("/users")
    response = response.json()
    print(response)
    assert isinstance(response, list)
    for user in response:
        if "id" in user:
            categories_json = {
                "hcs": random.randint(0, 1000000000),
                "food": random.randint(0, 1000000000),
                "transport": random.randint(0, 1000000000),
                "pharmacy": random.randint(0, 1000000000),
                "credits": random.randint(0, 1000000000),
                "fun": random.randint(0, 1000000000),
                "cloth": random.randint(0, 1000000000),
                "financial_cushion": random.randint(0, 1000000000),
                "target": random.randint(0, 1000000000),
                "date": datetime.datetime.utcnow(),
                "user_id": user["id"]
            }

            response_category = await client.post("/categories", json=categories_json)

            assert response_category.status_code == 200
            response_category = response_category.json()
            assert isinstance(response_category, dict)

# get tests

@pytest.mark.order(4)
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

@pytest.mark.order(5)
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


@pytest.mark.order(6)
async def test_get_categories(client: AsyncClient):
    categories = await client.get("/categories")
    assert categories.status_code == 200
    categories = categories.json()
    assert isinstance(categories, list)

    keys = ["hcs", "food", "transport", "pharmacy", "credits", "fun", " cloth", "financial_cushion", "target", "date", "id", "user_id"]

    for category in categories:
        for key in keys:
            assert key in category

@pytest.mark.order(7)
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

@pytest.mark.order(8)
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

# test errors

@pytest.mark.order(9)
async def test_get_user_by_id_error_not_found(client: AsyncClient):
    id = random.randint(1000000, 1000000*5)
    response = await client.get(f"/users/{id}")
    assert response.status_code == 404
    response = response.json()

    assert response["detail"] == "User not found"






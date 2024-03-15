import asyncio
import json
import sys
from typing import AsyncIterator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import insert, text

from app.config import settings
from app.database import async_session_maker, engine
from app.main import app
from app.models.base import Base
from app.models.referral_code import ReferralCode
from app.models.user import User

# from fastapi.testclient import TestClient
# from httpx import AsyncClient


@pytest_asyncio.fixture(autouse=True, scope="session")
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    users_list = open_mock_json("user")
    referral_code = open_mock_json("referral_code")

    async with async_session_maker() as session:
        for model, values, table_name, init_id in [
            (User, users_list, "user", True),
            (ReferralCode, referral_code, "referral_code", True),
        ]:
            query = insert(model).values(values)
            await session.execute(query)
            if init_id:
                await session.execute(
                    text(
                        f"SELECT SETVAL('{table_name}_id_seq',"
                        f' COALESCE((SELECT MAX(id) FROM "{table_name}"),1));'
                    )
                )
        await session.commit()

    # yield
    # удаление всех таблиц после тестов в БД
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)


# SETUP
# @pytest.fixture(scope="session")
# def event_loop(request):
#     """Create an instance of the default event loop for each test case."""
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for each test case."""
    if sys.platform == "win32" and sys.version_info.minor >= 8:
        policy = asyncio.WindowsSelectorEventLoopPolicy()
    else:
        policy = asyncio.get_event_loop_policy()
    res = policy.new_event_loop()
    asyncio.set_event_loop(res)
    res._close = res.close
    res.close = lambda: None
    yield res
    res._close()


# Фикстура асинхронного клиента для каждого из тестов
@pytest.fixture(autouse=True, scope="session")
async def ac() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


# Фикстура аутентифицированного клиента для каждого из тестов
@pytest.fixture(autouse=True, scope="session")
async def user_ac() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post(
            "/api/v1/auth/login",
            data={
                "username": "user1@example.com",
                "password": "user1",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        token = res.json().get("access_token")
        ac.headers.update({"Authorization": f"Bearer {token}"})
        yield ac

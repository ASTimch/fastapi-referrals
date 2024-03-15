import pytest
from httpx import AsyncClient

from app.config import settings


@pytest.mark.parametrize("route", [settings.API_V1_PREFIX + "/auth/me"])
async def test_me_authorized(route, user_ac: AsyncClient):
    response = await user_ac.get(route)
    assert response.status_code == 200


@pytest.mark.parametrize("route", [settings.API_V1_PREFIX + "/auth/me"])
async def test_me_unauthorized(route, ac: AsyncClient):
    response = await ac.get(route)
    assert response.status_code == 401


@pytest.mark.parametrize("route", [settings.API_V1_PREFIX + "/auth/login"])
async def test_login_success(route, ac: AsyncClient):
    response = await ac.post(
        route,
        data={
            "username": "user1@example.com",
            "password": "user1",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200


@pytest.mark.parametrize("route", [settings.API_V1_PREFIX + "/auth/login"])
async def test_login_invalid_password(route, ac: AsyncClient):
    response = await ac.post(
        route,
        data={
            "username": "user1@example.com",
            "password": "wrong_pass",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 401


@pytest.mark.parametrize("route", [settings.API_V1_PREFIX + "/auth/login"])
async def test_login_invalid_email(route, ac: AsyncClient):
    response = await ac.post(
        route,
        data={
            "username": "unknown@example.com",
            "password": "wrong_pass",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 401


@pytest.mark.parametrize("route", [settings.API_V1_PREFIX + "/auth/register"])
async def test_register_existent_email(route, ac: AsyncClient):
    response = await ac.post(
        route,
        json={
            "email": "user1@example.com",
            "password": "new_pass",
        },
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 409

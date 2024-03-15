import pytest
from httpx import AsyncClient

from app.config import settings

code_json = {"code_lifetime": 30}

user_id1_referrals = {
    "referrals": [
        {"id": 2, "email": "user2@example.com"},
        {"id": 3, "email": "user3@example.com"},
    ]
}
user_id2_referrals = {"referrals": []}

user_id1_refcode = {"id": 1, "code": "refcode1"}
user_id2_refcode = {"id": 2, "code": "refcode2"}


referral_code_route = settings.API_V1_PREFIX + "/referral_code"
referrals_route = settings.API_V1_PREFIX + "/referrals"


@pytest.mark.parametrize("route", [referral_code_route])
async def test_referral_code_anonym(route, ac: AsyncClient):
    response = await ac.post(route, json=code_json)
    assert response.status_code == 401
    response = await ac.get(route)
    assert response.status_code == 401
    response = await ac.delete(route)
    assert response.status_code == 401


@pytest.mark.parametrize(
    "route, user_id, referrals",
    [
        (referrals_route, 1, user_id1_referrals),
        (referrals_route, 2, user_id2_referrals),
    ],
)
async def test_referrals_for_user_id(
    route, user_id, referrals, ac: AsyncClient
):
    response = await ac.get(route + f"/{user_id}")
    assert response.status_code == 200
    assert response.json() == referrals


@pytest.mark.parametrize("route", [settings.API_V1_PREFIX + "/referral_code"])
async def test_get_referral_code_user(route, user_ac: AsyncClient):
    response = await user_ac.get(route)
    assert response.status_code == 200
    assert response.json() == user_id1_refcode


@pytest.mark.parametrize(
    "route, email, refcode, status",
    [
        (referral_code_route, "user1@example.com", user_id1_refcode, 200),
        (referral_code_route, "user2@example.com", user_id2_refcode, 200),
        (referral_code_route, "user3@example.com", None, 404),
        (referral_code_route, "unknown@example.com", None, 404),
    ],
)
async def test_get_referral_code_by_email(
    route, email, refcode, status, ac: AsyncClient
):
    response = await ac.get(route + f"/{email}")
    assert response.status_code == status
    if status == 200:
        assert response.json() == refcode

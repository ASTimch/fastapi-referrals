import asyncio

import pytest

from app.common.exceptions import (
    ReferralCodeExpiredException,
    ReferralCodeNotFoundException,
)
from app.crud.referral_code_dao import ReferralCodeDAO
from app.crud.user_dao import UserDAO
from app.services.referral_code import ReferralCodeService

refcode1 = {"id": 1, "code": "refcode1", "user_id": 1}
refcode2 = {"id": 2, "code": "refcode2", "user_id": 2}

dummy_user = {
    "email": "dummy@example.com",
    "hashed_password": "dummy",
}


@pytest.mark.parametrize(
    "id, ref_code_dict",
    [(1, refcode1), (2, refcode2)],
)
async def test_referral_code_service_get_by_id(id, ref_code_dict):
    dto = await ReferralCodeService.get_by_id(id)
    assert dto
    assert dto.id == ref_code_dict["id"]
    assert dto.code == ref_code_dict["code"]


@pytest.mark.parametrize("id", [(100)])
async def test_get_by_id_raises_exception_for_unknown_id(id):
    with pytest.raises(ReferralCodeNotFoundException):
        await ReferralCodeService.get_by_id(id)


@pytest.mark.parametrize(
    "user_id, ref_code_dict",
    [(1, refcode1), (2, refcode2)],
)
async def test_referral_code_service_get_by_user_id(user_id, ref_code_dict):
    dto = await ReferralCodeService.get_by_user_id(user_id)
    assert dto
    assert dto.id == ref_code_dict["id"]
    assert dto.code == ref_code_dict["code"]


@pytest.mark.parametrize("user_id", [(100), (3)])
async def test_get_by_user_id_raises_exception_if_code_not_found(user_id):
    with pytest.raises(ReferralCodeNotFoundException):
        await ReferralCodeService.get_by_user_id(user_id)


@pytest.mark.parametrize(
    "email, ref_code_dict",
    [("user1@example.com", refcode1), ("user2@example.com", refcode2)],
)
async def test_referral_code_service_get_by_user_email(email, ref_code_dict):
    dto = await ReferralCodeService.get_by_user_email(email)
    assert dto
    assert dto.id == ref_code_dict["id"]
    assert dto.code == ref_code_dict["code"]


@pytest.mark.parametrize(
    "email", [("user3@example.com"), ("unknown@example.com")]
)
async def test_get_by_user_email_raises_exception_if_code_not_found(email):
    with pytest.raises(ReferralCodeNotFoundException):
        await ReferralCodeService.get_by_user_email(email)


async def test_renew_and_delete_by_id():
    # create new dummy user
    user = await UserDAO.create(**dummy_user)
    code_dto = await ReferralCodeService.renew_user_code(user, life_time=30)
    assert code_dto
    user_id = await ReferralCodeService.get_referrer_user_id(code_dto.code)
    assert user_id == user.id, "Ошибка декодирования реферального кода"
    # удаляем код и пользователя из базы
    await ReferralCodeService.delete_by_id(code_dto.id)
    code = await ReferralCodeDAO.get_by_id(code_dto.id)
    assert not code, "Код не удален из базы"
    await UserDAO.delete_(user.id)


async def test_code_service_delete_by_user_id():
    # create new dummy user
    user = await UserDAO.create(**dummy_user)
    code_dto = await ReferralCodeService.renew_user_code(user, life_time=30)
    assert code_dto
    await ReferralCodeService.get_referrer_user_id(code_dto.code)
    # удаляем код из базы
    await ReferralCodeService.delete_by_user_id(user.id)
    code = await ReferralCodeDAO.get_by_id(code_dto.id)
    assert not code, "Код не удален из базы"
    await UserDAO.delete_(user.id)


async def test_referrer_user_id_raises_exception_for_expired_code():
    # create new dummy user
    user = await UserDAO.create(**dummy_user)
    code_dto = await ReferralCodeService.renew_user_code(user, life_time=0)
    assert code_dto
    await asyncio.sleep(1)
    with pytest.raises(ReferralCodeExpiredException):
        await ReferralCodeService.get_referrer_user_id(code_dto.code)
    # удаляем код и пользователя из базы
    await ReferralCodeService.delete_by_id(code_dto.id)
    code = await ReferralCodeDAO.get_by_id(code_dto.id)
    assert not code, "Код не удален из базы"
    await UserDAO.delete_(user.id)

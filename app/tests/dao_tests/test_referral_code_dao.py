import pytest

from app.crud.referral_code_dao import ReferralCodeDAO


@pytest.mark.parametrize(
    "id, code, user_id, exists",
    [
        (1, "refcode1", 1, True),
        (2, "refcode2", 2, True),
        (100, "unknown_code", None, False),
    ],
)
async def test_referral_code_get_by_id(id, code, user_id, exists):
    code_obj = await ReferralCodeDAO.get_by_id(id)
    if exists:
        assert code_obj
        assert id == code_obj.id
        assert code == code_obj.code
        assert user_id == code_obj.user_id
    else:
        assert not code_obj


@pytest.mark.parametrize(
    "id, code, user_id, exists",
    [
        (1, "refcode1", 1, True),
        (2, "refcode2", 2, True),
        (100, "unknown_code", None, False),
    ],
)
async def test_referral_code_get_user_id(id, code, user_id, exists):
    code_obj = await ReferralCodeDAO.get_by_user_id(user_id)
    if exists:
        assert code_obj
        assert id == code_obj.id
        assert code == code_obj.code
        assert user_id == code_obj.user_id
    else:
        assert not code_obj


@pytest.mark.parametrize(
    "code, user_id",
    [
        ("new_refcode", 3),
    ],
)
async def test_create_delete_upate_ref_code(code, user_id):
    obj = await ReferralCodeDAO.create(code=code, user_id=user_id)
    assert obj, "Функция не вернула созданный объект"
    assert obj.code == code
    assert obj.user_id == user_id
    # Чтение записи по id из базы
    id = obj.id
    obj = await ReferralCodeDAO.get_by_id(id)
    assert obj, "Объект не добавлен в базу"
    assert obj.id == id
    assert obj.code == code
    assert obj.user_id == user_id

    # Обновление
    code = code + "_updated"
    obj = await ReferralCodeDAO.update_(id, code=code)
    assert obj.code == code
    assert obj.user_id == user_id

    # удаление созданной записи
    await ReferralCodeDAO.delete_(id)
    obj = await ReferralCodeDAO.get_by_id(id)
    assert not obj, "Объект не удален из базы"

import pytest

from app.crud.user_dao import UserDAO

# from app.users.dao import UsersDAO


@pytest.mark.parametrize(
    "user_id, email, referrer_id, exists",
    [
        (1, "user1@example.com", None, True),
        (2, "user2@example.com", 1, True),
        (3, "user3@example.com", 1, True),
        (100, "unknown@example.com", None, False),
    ],
)
async def test_user_get_by_id(user_id, email, referrer_id, exists):
    user = await UserDAO.get_by_id(user_id)
    if exists:
        assert user
        assert user_id == user.id
        assert email == user.email
        assert referrer_id == user.referrer_id
    else:
        assert not user


@pytest.mark.parametrize(
    "user_id, email, exists",
    [
        (1, "user1@example.com", True),
        (2, "user2@example.com", True),
        (3, "user3@example.com", True),
        (100, "unknown@example.com", False),
    ],
)
async def test_user_get_one_or_none_by_email(user_id, email, exists):
    user = await UserDAO.get_one_or_none(email=email)
    if exists:
        assert user
        assert user_id == user.id
        assert email == user.email
    else:
        assert not user


@pytest.mark.parametrize(
    "referrer_id, referral_ids",
    [
        (1, (2, 3)),
        (2, ()),
        (3, ()),
    ],
)
async def test_user_get_all_by_referrer_id(referrer_id, referral_ids):
    referrals = await UserDAO.get_all(referrer_id=referrer_id)
    ids = [user.id for user in referrals]
    assert len(ids) == len(referral_ids)
    assert set(ids) == set(referral_ids)


@pytest.mark.parametrize(
    "email, hashed_password",
    [
        ("new_user@example.com", "any_password"),
    ],
)
async def test_create_delete_user(email, hashed_password):
    user = await UserDAO.create(email=email, hashed_password=hashed_password)
    assert user, "Функция не вернула созданный объект"
    assert user.email == email
    assert user.hashed_password == hashed_password
    # Чтение записи по id из базы
    id = user.id
    user = await UserDAO.get_by_id(id)
    assert user, "Объект не добавлен в базу"
    assert user.id == id
    assert user.email == email

    # удаление созданной записи
    await UserDAO.delete_(id)
    user = await UserDAO.get_by_id(id)
    assert not user, "Объект не удален из базы"

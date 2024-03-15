import pytest

from app.common.exceptions import UserAlreadyExistsException
from app.crud.user_dao import UserDAO
from app.schemas.auth import UserCreateDTO
from app.services.auth import AuthService, get_password_hash, verify_password

user2 = {
    "email": "user2@example.com",
    "password": "user2",
}

user1 = {
    "email": "user1@example.com",
    "password": "user1",
}


new_user4 = {
    "email": "user4@example.com",
    "password": "user4",
}


async def test_verify_password():
    pwd = "some_password"
    hashed_pwd = get_password_hash(pwd)
    assert pwd != hashed_pwd
    assert verify_password(pwd, hashed_pwd)
    assert not verify_password(pwd, hashed_pwd + "err")


async def test_register_new_user():
    user_data = UserCreateDTO(**new_user4)
    await AuthService.register(user_data)
    user = await UserDAO.get_one_or_none(email=new_user4["email"])
    assert user
    assert user.email == new_user4["email"]


@pytest.mark.parametrize(
    "user_dict",
    [(user1), (user2)],
)
async def test_register_existent_email_raises_exception(user_dict):
    with pytest.raises(UserAlreadyExistsException):
        user_data = UserCreateDTO(**user_dict)
        await AuthService.register(user_data)


@pytest.mark.parametrize(
    "email, id, exists",
    [
        ("user1@example.com", 1, True),
        ("user2@example.com", 2, True),
        ("unknown@example.com", None, False),
    ],
)
async def test_get_user_by_email(email, id, exists):
    user = await AuthService.get_user_by_email(email)
    if exists:
        assert user
        assert user.id == id
        assert user.email == email
    else:
        assert not user


@pytest.mark.parametrize(
    "email, password, id, result",
    [
        ("user1@example.com", "user1", 1, True),
        ("user1@example.com", "wrong", None, False),
        ("unknown@example.com", "any", None, False),
    ],
)
async def test_authenticate_user(email, password, id, result):
    user = await AuthService.authenticate_user(email, password)
    if result:
        assert user
        assert user.id == id
        assert user.email == email
    else:
        assert not user


@pytest.mark.parametrize(
    "referrer_id, users_id",
    [
        (1, (2, 3)),
        (2, ()),
        (3, ()),
    ],
)
async def test_get_users_by_referrer_id(referrer_id, users_id):
    dto = await AuthService.get_users_by_referrer_id(referrer_id)
    assert len(dto.referrals) == len(users_id)
    assert {user.id for user in dto.referrals} == set(users_id)

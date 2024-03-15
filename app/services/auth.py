from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.common.exceptions import (
    AuthorizationErrorException,
    UserAlreadyExistsException,
)
from app.config import settings
from app.crud.user_dao import UserDAO
from app.logger import logger
from app.models.user import User
from app.schemas.auth import ReferralsListDTO, UserCreateDTO, UserReadDTO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except ValueError as e:
        logger.exception(e, exc_info=True)
    return False


class AuthService:
    @classmethod
    async def register(
        cls,
        user_data: UserCreateDTO,
        referrer_id: int | None = None,
    ):
        """Регистрация нового пользователя.

        Args:
            user_data: Учетные данные пользователя.
            referrer_id: Уникальный идентификатор реферера.
        """
        existing_user = await UserDAO.get_one_or_none(email=user_data.email)
        if existing_user:
            raise UserAlreadyExistsException()
        hashed_password = get_password_hash(
            user_data.password.get_secret_value()
        )
        await UserDAO.create(
            email=user_data.email,
            hashed_password=hashed_password,
            referrer_id=referrer_id,
        )

    @classmethod
    async def authenticate_user(
        cls, email: EmailStr, password: str
    ) -> Optional[User]:
        user = await UserDAO.get_one_or_none(email=email)
        if user and verify_password(password, user.hashed_password):
            return user
        return None

    @classmethod
    async def get_user_by_email(cls, email: EmailStr) -> Optional[User]:
        return await UserDAO.get_one_or_none(email=email)

    @classmethod
    async def get_users_by_referrer_id(
        cls, referrer_id: int
    ) -> ReferralsListDTO:
        users = await UserDAO.get_all(referrer_id=referrer_id)
        return ReferralsListDTO(referrals=users)

    @classmethod
    def user_info(cls, user: User) -> UserReadDTO:
        return UserReadDTO.model_validate(user)

    @classmethod
    def create_access_token(cld, user: User) -> str:
        to_encode = {"sub": str(user.id)}
        expire = datetime.now(timezone.utc) + timedelta(
            seconds=settings.JWT_LIFETIME_SECONDS
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, settings.ALGORITHM
        )
        return encoded_jwt


async def current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    except JWTError:
        raise AuthorizationErrorException()
    user_id_str: str = payload.get("sub")
    if user_id_str is None:
        raise AuthorizationErrorException()
    user_id = int(user_id_str)
    user = await UserDAO.get_by_id(user_id)
    if user is None:
        raise AuthorizationErrorException()
    return user

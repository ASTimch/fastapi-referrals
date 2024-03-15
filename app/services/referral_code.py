from datetime import datetime, timedelta, timezone

from fastapi_cache.decorator import cache
from jose import jwt
from pydantic import EmailStr

from app.common.constants import Messages
from app.common.exceptions import (
    ReferralCodeExpiredException,
    ReferralCodeNotFoundException,
)
from app.config import settings
from app.crud.referral_code_dao import ReferralCodeDAO
from app.crud.user_dao import UserDAO
from app.models.base import pk_type
from app.models.user import User
from app.schemas.referral_code import ReferralCodeReadDTO


class ReferralCodeService:
    @classmethod
    async def generate_code(cls, user_id: pk_type, life_time: int) -> str:
        """Генерирует реферальный код для пользователя.

        Args:
            user_id: Идентификатор пользователя.
            life_time: Срок жизни реферального кода (минут).
        Returns:
            Реферальный код.

        """
        expire = datetime.now(timezone.utc) + timedelta(minutes=life_time)
        payload = {"sub": str(user_id), "exp": expire}
        referral_code = jwt.encode(
            payload, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return referral_code

    @classmethod
    @cache(expire=settings.CACHE_EXPIRE)
    async def get_by_id(cls, id: pk_type) -> ReferralCodeReadDTO:
        """Возвращает реферальный код с заданным идентификатором.

        Args:
            id (pk_type): идентификатор объекта в БД.

        Returns:
            ReferralCodeReadDTO: реферальный код с заданным id.

        Raises:
            ReferralCodeNotFoundException: если код заданным id не найден.
        """

        obj = await ReferralCodeDAO.get_by_id(id)
        if not obj:
            raise ReferralCodeNotFoundException()
        return ReferralCodeReadDTO.model_validate(obj)

    @classmethod
    @cache(expire=settings.CACHE_EXPIRE)
    async def get_by_user_id(cls, user_id: pk_type) -> ReferralCodeReadDTO:
        """Возвращает реферальный код для заданного пользователя.

        Args:
            user_id: Идентификатор пользователя в БД.

        Returns:
            ReferralCodeReadDTO: реферальный код пользователя.

        Raises:
            ReferralCodeNotFoundException: если код для пользователя не найден.
        """

        referral_code = await ReferralCodeDAO.get_by_user_id(user_id)
        if not referral_code:
            raise ReferralCodeNotFoundException()
        return ReferralCodeReadDTO.model_validate(referral_code)

    @classmethod
    @cache(expire=settings.CACHE_EXPIRE)
    async def get_by_user_email(cls, email: EmailStr) -> ReferralCodeReadDTO:
        """Возвращает реферальный код для заданного email пользователя.

        Args:
            email: email адрес пользователя.

        Returns:
            ReferralCodeReadDTO: Реферальный код пользователя.

        Raises:
            ReferralCodeNotFoundException: если код для пользователя не найден.
        """

        user = await UserDAO.get_one_or_none(email=email)
        if not user:
            raise ReferralCodeNotFoundException()
        referral_code = await ReferralCodeDAO.get_by_user_id(user.id)
        if not referral_code:
            raise ReferralCodeNotFoundException()
        return ReferralCodeReadDTO.model_validate(referral_code)

    @classmethod
    async def renew_user_code(
        cls, user: User, life_time: int
    ) -> ReferralCodeReadDTO:
        """Обновляет реферальный код для пользователя.

        Args:
            user: Пользователь, для которого обновляется/генерируется код.
            life_time: Срок жизни реферального кода (минут).

        Returns:
            ReferralCodeReadDTO: Реферальный код пользователя.
        """

        new_code = await cls.generate_code(user.id, life_time)
        old_code = await ReferralCodeDAO.get_by_user_id(user.id)
        if old_code:
            new_code = await ReferralCodeDAO.update_(
                old_code.id,
                code=new_code,
            )
        else:
            new_code = await ReferralCodeDAO.create(
                user_id=user.id,
                code=new_code,
            )
        return ReferralCodeReadDTO.model_validate(new_code)

    @classmethod
    async def delete_by_id(cls, id: pk_type):
        """Удалить реферальный код с заданным идентификатором.

        Args:
            id: идентификатор удаляемого объекта.

        Raises:
            ReferralCodeNotFoundException: если код с заданным id не найден.

        """
        referral_code = await ReferralCodeDAO.get_by_id(id)
        if not referral_code:
            raise ReferralCodeNotFoundException(
                detail=Messages.REFERRAL_CODE_FOR_USER_NOT_FOUND
            )
        await ReferralCodeDAO.delete_(id)

    @classmethod
    async def delete_by_user_id(cls, user_id: pk_type):
        """Удалить реферальный код для заданного пользователя.

        Args:
            user_id: Идентификатор пользователя.

        Raises:
            ReferralCodeNotFoundException: Если код для пользователя не найден.

        """
        referral_code = await ReferralCodeDAO.get_by_user_id(user_id)
        if not referral_code:
            raise ReferralCodeNotFoundException(
                detail=Messages.REFERRAL_CODE_FOR_USER_NOT_FOUND
            )
        await ReferralCodeDAO.delete_(referral_code.id)

    @classmethod
    async def get_referrer_user_id(cls, referral_code: str) -> pk_type:
        """Возвращает user_id для валидного реферального кода.

        Args:
            referral_code: Реферальный код.

        Returns:
            Идентификатор пользователя выдавшего код.

        Raises:
            ReferralCodeNotFoundException: Если код для пользователя не найден.
            ReferralCodeExpiredException: Если время жизни кода истекло.
        """
        if not referral_code:
            raise ReferralCodeNotFoundException()
        try:
            payload = jwt.decode(
                referral_code,
                key=settings.SECRET_KEY,
                algorithms=settings.ALGORITHM,
            )
            user_id = int(payload.get("sub"))
        except jwt.ExpiredSignatureError:
            raise ReferralCodeExpiredException()
        except jwt.JWTError:
            raise ReferralCodeNotFoundException()
        user_code_in_db = await ReferralCodeDAO.get_by_user_id(user_id)
        if not user_code_in_db or user_code_in_db.code != referral_code:
            raise ReferralCodeNotFoundException()
        return user_id

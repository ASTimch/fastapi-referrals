from typing import Optional

from sqlalchemy import Result, select
from sqlalchemy.orm import joinedload

from app.crud.base_dao import BaseDAO
from app.database import async_session_maker
from app.models.base import pk_type
from app.models.referral_code import ReferralCode


class ReferralCodeDAO(BaseDAO):
    model = ReferralCode

    @classmethod
    async def get_by_id(cls, id: pk_type) -> Optional[ReferralCode]:
        """Получить реферальный код с заданным идентификатором.

        Args:
            id (pk_type): идентификатор записи.

        Returns:
            ReferralCode | None: объект ReferralCode заданным id.
        """
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .filter_by(id=id)
                .options(joinedload(ReferralCode.user))
            )
            result: Result = await session.execute(query)
            return result.unique().scalar_one_or_none()

    @classmethod
    async def get_by_user_id(cls, user_id: pk_type) -> Optional[ReferralCode]:
        """Получить реферальный код для заданного идентификатора пользователя.

        Args:
            user_id (pk_type): идентификатор пользователя.

        Returns:
            ReferralCode | None: объект ReferralCode заданным user_id.
        """
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .filter_by(user_id=user_id)
                .options(joinedload(ReferralCode.user))
            )
            result: Result = await session.execute(query)
            return result.unique().scalar_one_or_none()

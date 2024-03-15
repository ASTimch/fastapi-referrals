from typing import Optional

from sqlalchemy import Result, select
from sqlalchemy.orm import selectinload, joinedload

from app.crud.base_dao import BaseDAO
from app.database import async_session_maker
from app.models.base import pk_type
from app.models.user import User


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def get_by_id(cls, id: pk_type) -> Optional[User]:
        """Получить пользователя с заданным идентификатором.

        Args:
            id (pk_type): идентификатор запрашиваемого пользователя.

        Returns:
            User | None: пользователь с заданным id.
        """
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .filter_by(id=id)
                .options(joinedload(User.referrer))
                .options(joinedload(User.referral_code))
                .options(selectinload(User.referrals))
            )
            result: Result = await session.execute(query)
            return result.unique().scalar_one_or_none()

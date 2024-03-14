from typing import TYPE_CHECKING, Optional
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, pk_type

if TYPE_CHECKING:
    from app.models.referral_code import ReferralCode


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    name: Mapped[str] = mapped_column(String(length=255), nullable=False)
    # referrers
    referral_code: Mapped[Optional["ReferralCode"]] = relationship(
        "ReferralCode", back_populates="user", uselist=False
    )
    referrer_id: Mapped[Optional[pk_type]] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True,
    )
    referrer: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="referrals",
        remote_side=[id],
    )
    referrals: Mapped[list["User"]] = relationship(
        "User",
        back_populates="referrer",
    )

    def __str__(self):
        return self.email

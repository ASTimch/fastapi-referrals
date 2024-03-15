from typing import Optional
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, pk_type

from app.models.referral_code import ReferralCode


class User(Base):
    __tablename__ = "user"
    id: Mapped[pk_type] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
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

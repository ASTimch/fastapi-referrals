from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, pk_type

if TYPE_CHECKING:
    from app.models.user import User


class ReferralCode(Base):
    """Реферальные коды."""

    __tablename__ = "referral_code"

    code: Mapped[str]
    user_id: Mapped[pk_type] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), unique=True
    )
    user: Mapped["User"] = relationship(
        back_populates="referral_code", uselist=False
    )

    def __str__(self):
        return f"{self.code}"

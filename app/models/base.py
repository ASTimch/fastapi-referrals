from typing import TypeAlias

from sqlalchemy import Integer, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


pk_type: TypeAlias = int


class Base(DeclarativeBase):
    __abstract__ = True
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )

    id: Mapped[pk_type] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    def to_dict(self):
        return {
            field.name: getattr(self, field.name) for field in self.__table__.c
        }

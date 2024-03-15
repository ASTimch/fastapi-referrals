from typing import TypeAlias

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

pk_type: TypeAlias = int


class Base(DeclarativeBase):
    __abstract__ = True
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",  # noqa E501
            "pk": "pk_%(table_name)s",
        }
    )

    def to_dict(self):
        return {
            field.name: getattr(self, field.name) for field in self.__table__.c
        }

from typing import Annotated, Union

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field

ReferralCodeQuery = Annotated[Union[str, None], Query(title="Реферальный код")]


class ReferralCodeReadDTO(BaseModel):
    """Реферальный код для чтения."""

    model_config = ConfigDict(from_attributes=True)
    id: Annotated[int, Field(description="Идентификатор")]
    code: Annotated[str, Field(description="Реферальный код")]


class ReferralCodeWriteDTO(BaseModel):
    """Реферальный код для записи."""

    model_config = ConfigDict(from_attributes=True)
    code_lifetime: Annotated[int, Field(description="Срок жизни кода (минут)")]

from typing import Annotated, List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr


UserEmail = Annotated[EmailStr, Field(description="email адрес")]


class Token(BaseModel):
    access_token: str
    token_type: str


class ReferralReadDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Annotated[int, Field(description="Идентификатор реферала")]
    email: UserEmail


class ReferralsListDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    referrals: Annotated[List[ReferralReadDTO], Field(description="Рефералы")]


class UserReadDTO(ReferralsListDTO):
    model_config = ConfigDict(from_attributes=True)
    id: Annotated[int, Field(description="Идентификатор пользователя")]
    email: UserEmail
    referrer: Annotated[
        Optional[ReferralReadDTO], Field(description="Реферер")
    ]


class UserAuthDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: UserEmail
    password: Annotated[SecretStr, Field(description="Пароль")]


class UserCreateDTO(UserAuthDTO):
    pass

from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.common.exceptions import (
    AuthorizationErrorException,
    ReferralCodeNotFoundException,
)
from app.config import settings
from app.logger import logger
from app.models.user import User
from app.schemas.auth import Token, UserCreateDTO, UserReadDTO
from app.schemas.referral_code import ReferralCodeQuery
from app.services.auth import AuthService, current_user
from app.services.referral_code import ReferralCodeService

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreateDTO, referral_code: ReferralCodeQuery = None
):
    referrer_id = None
    if referral_code:
        try:
            referrer_id = await ReferralCodeService.get_referrer_user_id(
                referral_code
            )
        except ReferralCodeNotFoundException as e:
            logger.exception(e, exc_info=True)
    await AuthService.register(user_data, referrer_id)


@router.post("/logout", status_code=200)
async def logout_user(response: Response):
    response.delete_cookie(settings.COOKIE_NAME)
    return {"result": "logout completed"}


@router.get("/me")
async def get_user_me(user: User = Depends(current_user)) -> UserReadDTO:
    return AuthService.user_info(user)


@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = await AuthService.authenticate_user(
        form_data.username,
        form_data.password,
    )
    if not user:
        raise AuthorizationErrorException()
    access_token = AuthService.create_access_token(user)
    return Token(access_token=access_token, token_type="bearer")

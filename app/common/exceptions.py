from fastapi import HTTPException, status

from app.common.constants import Messages


class ReferralException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self, detail=None):
        if detail:
            self.detail = detail
        super().__init__(status_code=self.status_code, detail=self.detail)


class ReferralCodeNotFoundException(ReferralException):
    """Реферальный код не найден в базе данных."""

    status_code = status.HTTP_404_NOT_FOUND
    detail = Messages.REFERRAL_CODE_NOT_FOUND


class ReferralCodeExpiredException(ReferralException):
    """Срок жизни кода истек."""

    status_code = status.HTTP_400_BAD_REQUEST
    detail = Messages.REFERRAL_CODE_EXPIRED


class AuthorizationErrorException(ReferralException):
    """Ошибка авторизации."""

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = Messages.AUTHORIZATION_ERROR


class AuthorizationErrorException(ReferralException):
    """Ошибка авторизации."""

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = Messages.AUTHORIZATION_ERROR


class UserAlreadyExistsException(ReferralException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"

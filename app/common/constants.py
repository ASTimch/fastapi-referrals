from typing import Final


class Messages:
    """Текстовые сообщения приложения"""

    REFERRAL_CODE_NOT_FOUND: Final = "Реферальный код не найден"
    REFERRAL_CODE_FOR_USER_NOT_FOUND: Final = (
        "Реферальный код для пользователя не найден"
    )
    REFERRAL_CODE_EXPIRED: Final = "Срок жизни реферального кода истек"
    AUTHORIZATION_ERROR: Final = "Ошибка авторизации"


class LogMessages:
    """Текстовые сообщения для логгированя"""

    RE_REGISRATION: Final = "Попытка повторной регистрации {}"
    NEW_REGISTRATION: Final = "Зарегистрирован новый пользователь {}"
    AUTHENTICATED: Final = "Пользователь {} аутентифицирован"
    AUTHENTICATION_FAILED: Final = "Ошибка аутентификации пользователя {}"
    REFCODE_UPDATED: Final = "Пользователь {} обновил реферальный код"
    REFCODE_CREATED: Final = "Пользователь {} создал реферальный код"
    USER_REFCODE_DELETED: Final = "Реферальный код {} пользователя {} удален"
    REFCODE_DELETED: Final = "Реферальный код {} удален"
    REFCODE_EMAILED: Final = "реферальный код отправлен на почту {}"

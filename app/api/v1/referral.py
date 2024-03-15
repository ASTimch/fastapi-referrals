from fastapi import APIRouter, BackgroundTasks, Depends, status

from app.models.user import User
from app.schemas.auth import UserEmail
from app.schemas.referral_code import ReferralCodeWriteDTO
from app.services.auth import AuthService, current_user
from app.services.email import send_referral_code_email
from app.services.referral_code import ReferralCodeService

referral_router = APIRouter()


@referral_router.post("/referral_code", summary="Создать реферальный код")
async def renew_referral_code(
    code: ReferralCodeWriteDTO,
    user: User = Depends(current_user),
):
    return await ReferralCodeService.renew_user_code(
        user=user,
        life_time=code.code_lifetime,
    )


@referral_router.get(
    "/referral_code", summary="Прочитать реферальный код текущего пользователя"
)
async def get_referral_code(user: User = Depends(current_user)):
    return await ReferralCodeService.get_by_user_id(user_id=user.id)


@referral_router.get(
    "/referral_code/{email}",
    summary="Получить реферальный код для заданного email",
)
async def get_referral_code_for_email(email: UserEmail):
    return await ReferralCodeService.get_by_user_email(email)


@referral_router.get(
    "/referrals/{referrer_id}",
    summary="Получить список всех рефералов по referrer_id",
)
async def get_referrals_by_referrer(referrer_id: int):
    return await AuthService.get_users_by_referrer_id(referrer_id)


@referral_router.get(
    "/email_referral_code",
    summary="Отправить реферальный код пользователя на почту",
)
async def email_referral_code(
    bg_tasks: BackgroundTasks, user: User = Depends(current_user)
):
    code_dto = await ReferralCodeService.get_by_user_id(user_id=user.id)
    bg_tasks.add_task(send_referral_code_email, user.email, code_dto.code)


@referral_router.get(
    "/validate_referral_code", summary="Валидировать реферальный код"
)
async def validate_referral_code(referral_code: str):
    return await ReferralCodeService.get_referrer_user_id(referral_code)


@referral_router.get(
    "/email_referral_code",
    summary="Отправить реферальный код на почту",
)
async def get_referral_code_by_email(
    user: User = Depends(current_user),
):
    return {"message": "Код будет отправлен на почту"}


@referral_router.delete(
    "/referral_code",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить реферальный код",
)
async def delete_referral_code(user: User = Depends(current_user)):
    await ReferralCodeService.delete_by_user_id(user.id)

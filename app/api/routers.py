from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.referral import referral_router
from app.config import settings

v1 = APIRouter(prefix=settings.API_V1_PREFIX)

v1.include_router(
    referral_router,
    prefix="",
    tags=["User referral"],
)

v1.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authorization"],
)

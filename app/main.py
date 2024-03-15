from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api import routers
from app.config import settings
from app.services.redis_cache import init_redis_cache


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_redis_cache()
    yield


app = FastAPI(
    title=settings.TITLE,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    openapi_url=settings.OPENAPI_URL,
    lifespan=lifespan,
)

app.include_router(routers.v1)

from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    # Postgresql
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    # Auth
    SECRET_KEY: str
    ALGORITHM: str
    JWT_LIFETIME_SECONDS: int = 3600
    # COOKIE_LIFETIME: int = 3600
    # COOKIE_NAME: str = "referral_access_token"
    # RESET_PASSWORD_SECRET: str
    CACHE_EXPIRE: int = 0

    # Redis
    REDIS_HOST: str
    REDIS_PORT: str

    # email smtp host
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    @property
    def database_url(self):
        return "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
            self.DB_USER,
            self.DB_PASS,
            self.DB_HOST,
            self.DB_PORT,
            self.DB_NAME,
        )

    @property
    def test_database_url(self):
        return "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
            self.TEST_DB_USER,
            self.TEST_DB_PASS,
            self.TEST_DB_HOST,
            self.TEST_DB_PORT,
            self.TEST_DB_NAME,
        )

    @property
    def redis_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    # Настройки приложения
    API_V1_PREFIX: str = "/api/v1"
    TITLE: str = "Referral application"
    VERSION: str = "0.0.1"
    DESCRIPTION: str = "Referral application"
    DOCS_URL: str | None = f"{API_V1_PREFIX}/docs"
    REDOC_URL: str | None = f"{API_V1_PREFIX}/redoc"
    OPENAPI_URL: str | None = f"{API_V1_PREFIX}/openapi"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )


settings = Settings()

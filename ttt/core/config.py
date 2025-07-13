# ttt/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SQLDB_URL: str
    SECRET_KEY: str
    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(
        env_file=".env.dev",  # ✅ ชัดเจนว่าใช้ .env.dev
        validate_assignment=True,
        extra="ignore",
    )


def get_settings():
    return Settings()

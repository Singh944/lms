import os
from functools import lru_cache


class Settings:
    APP_NAME: str = "Library Management System"
    ENV: str = os.getenv("ENV", "development")
    DEBUG: bool = ENV == "development"

    # DB
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./library.db")

    # Auth
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "change-me")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    # OAuth placeholders
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")


@lru_cache()
def get_settings() -> Settings:
    return Settings()



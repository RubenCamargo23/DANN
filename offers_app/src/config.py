import os
from functools import lru_cache


class Settings:
    """Application settings."""

    @classmethod
    @property
    @lru_cache()
    def app_name(cls) -> str:
        return os.getenv("APP_NAME", "Offers API")

    @classmethod
    @property
    @lru_cache()
    def log_level(cls) -> str:
        return os.getenv("LOG_LEVEL", "DEBUG")

    @classmethod
    @property
    def db_host(cls) -> str:
        return os.getenv("DB_HOST", "localhost")

    @classmethod
    @property
    def db_port(cls) -> str:
        return os.getenv("DB_PORT", "5432")

    @classmethod
    @property
    def db_user(cls) -> str:
        return os.getenv("DB_USER", "postgres")

    @classmethod
    @property
    def db_password(cls) -> str:
        return os.getenv("DB_PASSWORD", "postgres")

    @classmethod
    @property
    def db_name(cls) -> str:
        return os.getenv("DB_NAME", "offers_db")

    @classmethod
    @property
    def database_url(cls) -> str:
        return (
            f"postgresql://{cls.db_user}:{cls.db_password}"
            f"@{cls.db_host}:{cls.db_port}/{cls.db_name}"
        )

import os
from functools import lru_cache


class Settings:
    """Application settings."""

    @classmethod
    @property
    @lru_cache()
    def app_name(self) -> str:
        return os.getenv("APP_NAME", "Users API")

    @classmethod
    @property
    @lru_cache()
    def log_level(self) -> str:
        return os.getenv("LOG_LEVEL", "DEBUG")

    @classmethod
    @property
    def db_host(self) -> str:
        return os.getenv("DB_HOST", "localhost")

    @classmethod
    @property
    def db_port(self) -> str:
        return os.getenv("DB_PORT", "5432")

    @classmethod
    @property
    def db_user(self) -> str:
        return os.getenv("DB_USER", "postgres")

    @classmethod
    @property
    def db_password(self) -> str:
        return os.getenv("DB_PASSWORD", "postgres")

    @classmethod
    @property
    def db_name(self) -> str:
        return os.getenv("DB_NAME", "users_db")

    @classmethod
    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

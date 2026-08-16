import os


class Settings:
    """Application settings."""

    app_name = os.getenv("APP_NAME", "Users API")
    log_level = os.getenv("LOG_LEVEL", "DEBUG")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "postgres")
    db_name = os.getenv("DB_NAME", "users_db")
    database_url = (
        f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )

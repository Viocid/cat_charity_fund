from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = "Кошачий благотворительный фонд"
    app_description: str = (
        "Фонд собирает пожертвования на различные целевые проекты: на "
        "медицинское обслуживание нуждающихся хвостатых, на обустройство "
        "кошачьей колонии в подвале, на корм оставшимся без попечения кошкам "
        "— на любые цели, связанные с поддержкой кошачьей популяции."
    )
    database_url: str = "sqlite+aiosqlite:///./default.db"
    secret: str = "SECRET"
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    jwt_token_lifetime: int = 3600
    user_password_min_len: int = 3
    logging_format: str = "%(asctime)s - %(levelname)s - %(message)s"
    logging_dt_format: str = "%Y-%m-%d %H:%M:%S"

    class Config:
        env_file = ".env"


settings = Settings()

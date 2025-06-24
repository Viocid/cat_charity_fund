# app/core/validators.py
from typing import Union
from fastapi_users import InvalidPasswordException

from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate


def validate_password_length(password: str) -> None:
    if len(password) < settings.user_password_min_len:
        raise InvalidPasswordException(
            reason=
            f'Пароль должен быть длинее {settings.user_password_min_len} '
            f'символов'
        )


def validate_password_not_email(password: str, email: str) -> None:
    if email == password:
        raise InvalidPasswordException(
            reason='Пароль не должен совпадать с емейлом.'
        )


def validate_user_password(
    password: str,
    user: Union[UserCreate, User]
) -> None:
    email = user.email if isinstance(user, User) else user.email
    validate_password_length(password)
    validate_password_not_email(password, email)
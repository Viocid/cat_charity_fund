from typing import Optional

from pydantic import BaseModel, conint, Extra, Field, validator

from app.core.constants import NAME_MAX_LEN, NAME_MIN_LEN, ZERO
from app.schemas.mixins import DBMixin


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, max_length=NAME_MAX_LEN)
    description: Optional[str]
    full_amount: Optional[conint(gt=ZERO)]

    class Config:
        min_anystr_length = NAME_MIN_LEN


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., max_length=NAME_MAX_LEN)
    description: str
    full_amount: conint(gt=ZERO)


class CharityProjectUpdate(CharityProjectBase):
    @validator('name')
    def name_not_none(cls, value: Optional[str]):
        if value is None:
            raise ValueError('Название проекта не может быть пустым.')
        return value

    @validator('description')
    def description_not_none(cls, value: Optional[str]):
        if value is None:
            raise ValueError('Описание проекта не может быть пустым.')
        return value

    class Config:
        extra = Extra.forbid


class CharityProjectDB(DBMixin, CharityProjectCreate):
    """Схема для отображения проектов."""
    pass

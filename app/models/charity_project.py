from sqlalchemy import Column, String, Text

from app.core.constants import NAME_MAX_LEN
from app.models.base import CharityDonatBase


class CharityProject(CharityDonatBase):
    name = Column(String(NAME_MAX_LEN), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self) -> str:
        return (
            f'Проект "{self.name}": {self.invested_amount}/{self.full_amount}'
        )

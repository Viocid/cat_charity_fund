from sqlalchemy import Column, String, Text

from app.models.charitybase import CharityBase
from app.core.constants import NAME_MAX_LEN


class CharityProject(CharityBase):
    """Модель проекта."""
    name = Column(String(NAME_MAX_LEN), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self) -> str:
        return f'Проект "{self.name}": {self.invested_amount}/{self.full_amount}'

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, conint

from app.core.constants import ZERO


class DBMixin(BaseModel):
    """
    Миксина для общих полей схем полного отображения данных проектов и
     пожервований.
    """

    id: int
    invested_amount: conint(ge=ZERO) = Field(default=ZERO)
    fully_invested: bool = Field(default=False)
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, conint

from app.core.constants import ZERO
from app.schemas.mixins import DBMixin


class DonationCreate(BaseModel):
    full_amount: conint(gt=ZERO)
    comment: Optional[str]


class DonationOwnerView(DonationCreate):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DBMixin, DonationCreate):
    user_id: int

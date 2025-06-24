from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.constants import ZERO
from app.core.db import Base


class CharityDonatBase(Base):
    __abstract__ = True
    __table_args__ = (CheckConstraint("full_amount >= invested_amount"),)
    full_amount = Column(
        Integer, CheckConstraint("full_amount > 0"), nullable=False
    )
    invested_amount = Column(
        Integer,
        CheckConstraint("invested_amount >= 0"),
        default=ZERO,
        nullable=False,
    )
    fully_invested = Column(Boolean, default=False, nullable=False)
    create_date = Column(DateTime, default=datetime.now, index=True)
    close_date = Column(DateTime)

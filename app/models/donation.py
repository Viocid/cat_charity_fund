from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import CharityDonatBase


class Donation(CharityDonatBase):
    user_id = Column(
        Integer,
        ForeignKey("user.id", name="fk_donation_user_id_user"),
        nullable=False,
    )
    comment = Column(Text)

    def __repr__(self) -> str:
        return (
            f"Пожертвование от ID {self.user_id}: {self.invested_amount}/" +
            str(self.full_amount)
        )

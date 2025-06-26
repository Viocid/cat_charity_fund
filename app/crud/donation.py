from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    async def get_multi_for_current_user(
        self, user: User, session: AsyncSession
    ) -> list[Donation]:
        db_objs = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return db_objs.scalars().all()

    async def get_active_ordered(
        self, session: AsyncSession
    ) -> list[Donation]:
        result = await session.execute(
            select(Donation)
            .where(Donation.fully_invested is False)
            .order_by(Donation.create_date)
        )
        return result.scalars().all()

    async def update_investment(
        self, session: AsyncSession, first_donation: Donation
    ) -> Donation:
        await session.add(session, first_donation)
        return first_donation


donation_crud = CRUDDonation(Donation)

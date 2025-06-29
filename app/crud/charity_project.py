from datetime import datetime
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


class CRUDCharityProject(CRUDBase):

    async def get_charity_project_by_name(
        self, charity_project_name: str, session: AsyncSession
    ) -> Optional[CharityProject]:
        db_obj = await session.execute(
            select(CharityProject).where(
                CharityProject.name == charity_project_name
            )
        )
        return db_obj.scalars().first()

    async def update(
        self,
        db_obj: CharityProject,
        obj_in: CharityProjectUpdate,
        session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        if db_obj.invested_amount == db_obj.full_amount:
            db_obj.fully_invested = True
            db_obj.close_date = datetime.now()
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self, db_obj: CharityProject, session: AsyncSession
    ) -> CharityProject:
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_active_ordered(
        self, session: AsyncSession
    ) -> list[CharityProject]:
        result = await session.execute(
            select(CharityProject)
            .where(CharityProject.fully_invested is False)
            .order_by(CharityProject.create_date)
        )
        return result.scalars().all()

    async def update_investment(
        self, session: AsyncSession, first_project: CharityProject
    ) -> CharityProject:
        await session.add(session, first_project)
        return first_project

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ) -> list[CharityProject]:
        completion_duration = extract(
            "epoch", CharityProject.close_date
        ) - extract("epoch", CharityProject.create_date)
        statement = (
            select(CharityProject)
            .where(CharityProject.fully_invested is True)
            .order_by(completion_duration.asc())
        )
        db_objs = await session.execute(statement)
        return db_objs.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)

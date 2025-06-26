from datetime import datetime
from typing import Union

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import ONE, ZERO
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import CharityProject, Donation


def don_char(donations, projects, session):
    donation_index = ZERO
    project_index = ZERO
    len_donations = len(donations)
    len_projects = len(projects)
    while (
        donation_index < len_donations and
        project_index < len_projects
    ):
        first_donation = donations[donation_index]
        first_project = projects[project_index]
        donation_capacity = (
            first_donation.full_amount -
            first_donation.invested_amount
        )
        project_capacity = (
            first_project.full_amount -
            first_project.invested_amount
        )
        min_capacity = min(donation_capacity, project_capacity)
        first_donation.invested_amount += min_capacity
        first_project.invested_amount += min_capacity

        if (
            first_donation.invested_amount ==
            first_donation.full_amount
        ):
            first_donation.fully_invested = True
            first_donation.close_date = datetime.now()
            donation_index += ONE

        if (
            first_project.invested_amount ==
            first_project.full_amount
        ):
            first_project.fully_invested = True
            first_project.close_date = datetime.now()
            project_index += ONE
        session.add(first_donation)
        session.add(first_project)


async def investments(
    session: AsyncSession, new_db_obj: Union[CharityProject, Donation]
) -> Union[CharityProject, Donation]:
    """
    Функция распределения средств среди активных проектов и пожертвований.
    """
    try:
        donations = await donation_crud.get_active_order_by_create_date(
            session
        )
        projects = (
            await charity_project_crud.get_active_order_by_create_date(session)
        )
        if not (donations or projects):
            return
        don_char(donations, projects, session)

        await session.commit()
        await session.refresh(new_db_obj)
        return new_db_obj

    except SQLAlchemyError as error:
        await session.rollback()
        raise SQLAlchemyError(
            "В процессе распределения средств произошла ошибка."
        ) from error
    except Exception as error:
        await session.rollback()
        raise Exception(
            "В процессе распределения средств произошла ошибка."
        ) from error

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import DOCS_URL
from app.core.db import get_async_session
from app.core.google_client import get_service
from app.crud.charity_project import charity_project_crud
from app.services.google import (set_user_permissions, spreadsheets_create,
                                 spreadsheets_update_value)
from app.services.utils import url

router = APIRouter()


@router.post(
    "/",
    summary="Создание отчета в Google-таблицах.",
    response_description="Ссылка на созданный отчет.",
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services=Depends(get_service),
):
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )

    spreadsheet_id = await spreadsheets_create(wrapper_services)

    await set_user_permissions(spreadsheet_id, wrapper_services)

    await spreadsheets_update_value(
        spreadsheet_id=spreadsheet_id,
        projects=projects,
        wrapper_services=wrapper_services,
    )

    return {"report_url": url(DOCS_URL, spreadsheet_id)}

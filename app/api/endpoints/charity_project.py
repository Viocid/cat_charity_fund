from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (project_active, project_exists,
                                project_name_duplicate,
                                project_new_full_amount, project_not_invested)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investments import investments

router = APIRouter()


@router.get(
    path="/",
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_multi(session=session)


@router.post(
    path="/",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=(Depends(current_superuser),),
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await project_name_duplicate(
        charity_project_name=charity_project.name, session=session
    )
    new_charity_project = await charity_project_crud.create(
        obj_in=charity_project, session=session
    )
    return await investments(session=session, new_db_obj=new_charity_project)


@router.delete(
    path="/{project_id}",
    response_model=CharityProjectDB,
    dependencies=(Depends(current_superuser),),
)
async def delete_charity_project(
    project_id: int, session: AsyncSession = Depends(get_async_session)
):
    charity_project = await project_exists(
        charity_project_id=project_id, session=session
    )
    project_not_invested(charity_project=charity_project)
    return await charity_project_crud.remove(
        db_obj=charity_project, session=session
    )


@router.patch(
    path="/{project_id}",
    response_model=CharityProjectDB,
    dependencies=(Depends(current_superuser),),
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await project_exists(
        charity_project_id=project_id, session=session
    )
    project_active(charity_project=charity_project)
    if obj_in.name is not None:
        await project_name_duplicate(
            charity_project_name=obj_in.name, session=session
        )
    if obj_in.full_amount is not None:
        project_new_full_amount(
            charity_project=charity_project, new_full_amount=obj_in.full_amount
        )
    return await charity_project_crud.update(
        db_obj=charity_project, obj_in=obj_in, session=session
    )

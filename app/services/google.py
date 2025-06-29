from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.core.constants import DOCS_URL, FORMAT
from app.schemas.charity_project import CharityProjectDB


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover("sheets", "v4")
    now_time = datetime.now().strftime(FORMAT)
    spreadsheet_body = {
        "properties": {
            "title": f"Отчет от QRKot на {now_time}",
            "locale": "ru_RU",
        },
        "sheets": [
            {
                "properties": {
                    "sheetType": "GRID",
                    "sheetId": 0,
                    "title": "Лист 1",
                    "gridProperties": {"rowCount": 100, "columnCount": 11},
                }
            }
        ],
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response["spreadsheetId"]
    print(f"Создан документ: {DOCS_URL}{spreadsheet_id}")
    return spreadsheet_id


async def set_user_permissions(
    spreadsheet_id: str, wrapper_services: Aiogoogle
) -> None:

    service = await wrapper_services.discover("drive", "v3")

    permissions_body = {
        "type": "user",
        "role": "writer",
        "emailAddress": settings.email,
    }

    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields="id",
        )
    )
    print(
        f"Выданы права пользователю"
        f"{settings.email} на документ: {DOCS_URL}{spreadsheet_id}"
    )


async def spreadsheets_update_value(
    spreadsheet_id: str,
    projects: list[CharityProjectDB],
    wrapper_services: Aiogoogle,
) -> None:
    service = await wrapper_services.discover("sheets", "v4")
    now_time_for_report = datetime.now().strftime(FORMAT)
    table_values = [
        ["Отчет от", now_time_for_report],
        ["Топ проектов по скорости закрытия"],
        ["Название проекта", "Время сбора (дни)", "Описание"],
    ]

    for project in projects:
        duration = project.close_date - project.create_date
        days = duration.days
        seconds = duration.seconds
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"{days} дней, {hours}:{minutes:02d}:{seconds:02d}"
        table_values.append(
            [str(project.name), time_str, str(project.description)]
        )

    update_body = {"majorDimension": "ROWS", "values": table_values}

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range="A1",
            valueInputOption="USER_ENTERED",
            json=update_body,
        )
    )
    print(f"Данные успешно записаны в документ: {DOCS_URL}{spreadsheet_id}")

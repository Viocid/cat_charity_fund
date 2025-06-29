# Cat Charity Fund 🐱💙

Проект **Cat Charity Fund** — это платформа для сбора пожертвований в пользу кошачьих приютов. Пользователи могут создавать проекты для сбора средств, делать пожертвования и отслеживать собранные суммы.

## 🚀 Запуск проекта

### Требования
- Python 3.9+
- Docker (опционально, для запуска в контейнере)
- Установленный `poetry` (для управления зависимостями)

### Инструкция по установке

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/Viocid/cat_charity_fund.git
   cd cat_charity_fund
Установите зависимости:

bash
poetry install
Настройте переменные окружения:
Создайте файл .env в корне проекта и заполните его по примеру .env.example.

Примените миграции:

bash
alembic upgrade head
Запустите сервер:

bash
uvicorn app.main:app --reload
Сервер будет доступен по адресу: http://127.0.0.1:8000
Основные endpoints:
POST /projects/ - Создать новый проект

GET /projects/ - Получить список проектов

POST /donations/ - Сделать пожертвование

GET /donations/ - Получить список пожертвований

Google Sheets отчеты:
POST /google/ - Создать отчет в Google Sheets (только для суперюзеров)

Документация API доступна по адресу: http://127.0.0.1:8000/docs
📡 Примеры запросов
Создание проекта
bash
curl -X POST "http://127.0.0.1:8000/projects/" \
-H "Authorization: Bearer YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{"name": "Спасение котиков", "description": "Помогите бездомным котикам!", "full_amount": 5000}'
Получение списка проектов
bash
curl -X GET "http://127.0.0.1:8000/projects/" \
-H "Authorization: Bearer YOUR_TOKEN"
Создание пожертвования
bash
curl -X POST "http://127.0.0.1:8000/donations/" \
-H "Authorization: Bearer YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{"full_amount": 1000, "comment": "На корм котикам!"}'

🛠 Используемые технологии
Python + FastAPI (веб-фреймворк)

SQLAlchemy (ORM)

Alembic (миграции)

PostgreSQL (база данных)

Docker (контейнеризация)

Poetry (управление зависимостями)

Aiogoogle (работа с Google API)

👨‍💻 Автор
Viocid – разработчик и кошачий энтузиаст 🐾http://127.0.0.1:8000

Особенности реализации Google Sheets отчетов
Для работы с Google API необходимо:

Создать сервисный аккаунт в Google Cloud Console

Включить Google Sheets API и Google Drive API

Добавить в .env файл учетные данные сервисного аккаунта

Выдать права доступа вашему email на редактирование таблиц
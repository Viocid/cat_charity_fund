# Cat Charity Fund

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.78-009688)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4-red)
![Alembic](https://img.shields.io/badge/Alembic-migrations-orange)
![Pytest](https://img.shields.io/badge/Pytest-tested-green)

FastAPI backend service for charity project and donation management.

The application allows users to make donations to charity projects. Donations are automatically distributed between open projects according to the order in which donations and projects were created.

---

## Main features

- User registration and authentication
- JWT-based authorization
- Superuser-only charity project management
- Donation creation for authenticated users
- Automatic donation distribution between active projects
- User-specific donation history
- Google Sheets report generation
- Async SQLAlchemy database layer
- Alembic database migrations
- API validation with Pydantic schemas
- Automated tests with Pytest

---

## Tech stack

### Backend

- Python
- FastAPI
- FastAPI Users
- Pydantic

### Database

- SQLAlchemy
- Alembic
- SQLite by default
- PostgreSQL-compatible configuration through `DATABASE_URL`

### External integrations

- Google Sheets API
- Google Drive API
- Aiogoogle

### Testing and tools

- Pytest
- Pytest Asyncio
- Flake8
- Uvicorn

---

## Project structure

```text
cat_charity_fund/
├── alembic/                 # Database migrations
├── app/
│   ├── api/                 # API routers, endpoints and validators
│   ├── core/                # Config, database, users and Google client
│   ├── crud/                # Database access layer
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic and integrations
│   └── main.py              # FastAPI application entry point
├── tests/                   # Automated tests
├── openapi.json             # OpenAPI schema
├── alembic.ini              # Alembic configuration
└── requirements.txt
```

---

## API endpoints

### Charity projects

| Method | Endpoint | Description | Access |
|---|---|---|---|
| `GET` | `/charity_project/` | Get all charity projects | Public |
| `POST` | `/charity_project/` | Create a charity project | Superuser |
| `PATCH` | `/charity_project/{project_id}` | Update a charity project | Superuser |
| `DELETE` | `/charity_project/{project_id}` | Delete a charity project | Superuser |

### Donations

| Method | Endpoint | Description | Access |
|---|---|---|---|
| `GET` | `/donation/` | Get all donations | Superuser |
| `POST` | `/donation/` | Create a donation | Authenticated user |
| `GET` | `/donation/my` | Get current user's donations | Authenticated user |

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/register` | Register a new user |
| `POST` | `/auth/jwt/login` | Get JWT token |
| `POST` | `/auth/jwt/logout` | Logout |
| `GET` | `/users/me` | Get current user |
| `PATCH` | `/users/me` | Update current user |

### Reports

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/google/` | Create Google Sheets report with completed projects |

---

## Business logic

The core feature of the project is automatic investment distribution.

When a new donation or project is created, the service finds open donations and open charity projects, then distributes available amounts in creation order.

A project or donation becomes closed when its `invested_amount` reaches `full_amount`.

This demonstrates:

- service-layer business logic;
- transaction-like update flow;
- separated CRUD and API layers;
- validation before database updates.

---

## Local installation

Clone the repository:

```bash
git clone https://github.com/Viocid/cat_charity_fund.git
cd cat_charity_fund
```

Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` file in the project root:

```env
APP_TITLE=Cat Charity Fund
APP_DESCRIPTION=Charity donation API
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=your-secret-key
FIRST_SUPERUSER_EMAIL=admin@example.com
FIRST_SUPERUSER_PASSWORD=admin-password
```

Apply migrations:

```bash
alembic upgrade head
```

Run the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Google Sheets integration

The project can create reports in Google Sheets through a service account.

To enable this feature, configure Google API credentials in `.env`:

```env
TYPE=
PROJECT_ID=
PRIVATE_KEY_ID=
PRIVATE_KEY=
CLIENT_EMAIL=
CLIENT_ID=
AUTH_URI=
TOKEN_URI=
AUTH_PROVIDER_X509_CERT_URL=
CLIENT_X509_CERT_URL=
EMAIL=
```

The report contains completed charity projects sorted by completion speed.

---

## Running tests

```bash
pytest
```

---

## What this project demonstrates

- FastAPI backend development
- Async database interaction with SQLAlchemy
- Alembic migrations
- JWT authentication
- Role-based permissions
- Business logic in service layer
- External API integration
- Automated testing
- Clean project structure

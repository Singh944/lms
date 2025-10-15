## Library Management System (LMS)

A FastAPI-based system to manage books, users, and issue/return operations with authentication and dashboards.

### Features
- **Super Admin**: Email/password or Google SSO, upload Excel for books/users, full CRUD, view system stats
- **Normal User**: Google SSO, search/filter books, request borrow, view/return borrowed
- **Dashboards**: Admin (books/users/issued/logs), User (borrowed/history/recommendations)
- **Good-to-have**: Excel export, email reminders, ratings/reviews, autocomplete search

### Tech Stack
- **Backend**: FastAPI (Python)
- **Frontend**: Jinja2 templates (can be swapped for React later)
- **DB**: SQLite (dev) / PostgreSQL (prod)
- **Auth**: JWT (core), Google OAuth (scaffold)
- **Excel**: pandas, openpyxl

### Architecture Diagram
```mermaid
flowchart LR
  subgraph Client
    Browser["Web Browser"]
  end

  subgraph FastAPI["FastAPI App"]
    Routes["Routes and Controllers"]
    Services["Domain Services"]
    Auth["Auth (JWT and Google SSO)"]
    Templates["Jinja2 Templates"]
    Models["SQLAlchemy Models"]
  end

  subgraph Storage
    DB["Database: SQLite or PostgreSQL"]
    Files["Static / Uploads"]
  end

  Browser -->|HTTP/HTTPS| Routes
  Routes --> Services
  Routes --> Templates
  Services --> Models
  Auth --> Routes
  Models --> DB
  Routes --> Files
```

### Project Structure
```text
library_mgmt/
├── app/
│   ├── auth/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── utils/
│   └── templates/ (or frontend/)
├── static/
├── main.py
├── config.py
requirements.txt
README.md
.env (not committed) / .env.example
```

### Getting Started
1) Python setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Environment variables
Copy and adjust `.env.example` to `.env`.
```bash
cp .env.example .env
```

3) Run the server
```bash
uvicorn library_mgmt.main:app --reload
```
Visit: `http://localhost:8000/health` and `http://localhost:8000/docs`

4) Database
- Default is SQLite file `library.db` in project root
- To use Postgres, set `DATABASE_URL` in `.env`, e.g. `postgresql+psycopg://user:pass@localhost:5432/lms`

### Configuration
The app reads settings from environment variables (see `.env.example`). Key options:
- `DATABASE_URL`: SQLite or Postgres URL
- `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`
- `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` (for SSO scaffold)

### Development Notes
- SQLAlchemy models defined under `library_mgmt/app/models`
- DB engine/session under `library_mgmt/app/utils/db.py`
- Tables auto-created at startup for local dev

### Planned Endpoints (incremental)
- Auth: register/login (JWT), Google SSO scaffold
- Books: CRUD, search/filter
- Users: CRUD (admin), self-profile
- Issue/Return: create issue, return book, list borrowed/history
- Dashboards: admin and user views

### Excel Import/Export (planned)
- Import books/users from Excel via admin
- Export reports to Excel

### Deployment
- Uvicorn/Gunicorn example (Linux service or containerized):
```bash
uvicorn library_mgmt.main:app --host 0.0.0.0 --port 8000
```
- Set `ENV=production` and configure a production `DATABASE_URL`
- Behind Nginx/Traefik reverse proxy (TLS termination recommended)

### License
MIT (or update as preferred)



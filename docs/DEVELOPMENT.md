# Development

## Docker workflow

Copy `.env.example` to `.env`, replace `DJANGO_SECRET_KEY`, then run `docker compose up --build`. Docker is the reference environment because it supplies PostgreSQL and Redis.

## Native workflow

Frontend: from `frontend`, run `npm install`, `npm run dev`, `npm run lint`, and `npm run typecheck`.

Backend: create a Python 3.12 virtual environment, install `backend/requirements-dev.txt`, set environment variables, then from `backend` run `python manage.py migrate`, `python manage.py runserver`, `ruff check .`, and `pytest`.

Use PostgreSQL in normal development. SQLite may be selected only for isolated configuration checks through an explicit test environment; behavior relying on PostgreSQL must have PostgreSQL integration tests.

## Conventions

Domain behavior lives in its owning app. Keep views and Celery tasks thin, put transactions in application services, validate external input at boundaries, and add migrations plus tests with model changes. Never commit `.env`, credentials, recordings, or production exports.

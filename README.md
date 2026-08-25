# Careergize Pulse

Internal call-intelligence, tracking, analytics, and follow-up platform. Phase 0 establishes a modular-monolith foundation only; business features begin in later phases.

## Repository

- `frontend/` — Next.js web application
- `backend/` — Django/DRF API and Celery workers
- `docs/` — architecture, security, API, and operational decisions
- `docker/` — container definitions
- `docker-compose.yml` — local PostgreSQL, Redis, backend, worker, and frontend

## Quick start

1. Copy `.env.example` to `.env` and replace development-only secrets.
2. Run `docker compose up --build`.
3. Open the frontend at `http://localhost:3000` and API health endpoint at `http://localhost:8000/api/v1/health/`.

Native development instructions are in [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md). Architecture decisions are in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Phase boundary

Implemented: repository layout, configuration, domain boundaries, health checks, tenant-ready base models, provider interfaces, Celery wiring, Docker foundations, and documentation.

Not implemented: telephony provider integrations, call workflows, dashboards, billing, AI, public signup, or multi-workspace UI.

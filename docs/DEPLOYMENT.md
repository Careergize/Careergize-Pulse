# Deployment

## Frontend

Deploy `frontend/` to Vercel. Configure `NEXT_PUBLIC_API_URL` to the public backend `/api/v1` endpoint. Preview deployments should target non-production data.

## Backend

The backend image is portable to Azure Container Apps/App Service, AWS ECS/App Runner, Render, or Railway. Run the same image as web and Celery worker with different commands. Use managed PostgreSQL, managed Redis, and private S3-compatible storage. Run migrations as a single release job before/alongside a backward-compatible deployment.

Required production controls: TLS, trusted proxy configuration, secure cookies, explicit allowed hosts/origins, encrypted secrets, database backups with restore tests, storage lifecycle rules, centralized logs, health checks, alerting, worker monitoring, and least-privilege network access.

Horizontal web/worker scaling is stateless. Redis loss may delay work but must not lose authoritative state because raw webhook events are stored in PostgreSQL. Region and data residency decisions are made before production data ingestion.

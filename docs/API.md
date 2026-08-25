# API Architecture

The REST API is rooted at `/api/v1/`. JSON uses consistent error envelopes and cursor pagination for potentially large collections. OpenAPI generation is provided by drf-spectacular; published schemas become compatibility artifacts.

Endpoints are organized by domain, not database table. Views authenticate, authorize, validate, and delegate to application services. Serializers must not contain multi-domain workflows. Tenant identity is derived from the authenticated membership and selected organization context, never trusted from an arbitrary request body.

Phase 0 exposes only:

- `GET /api/v1/health/` — process liveness.
- `GET /api/v1/health/ready/` — database and Redis readiness.
- `GET /api/schema/` — OpenAPI schema.

Webhook endpoints will live under `/api/v1/webhooks/telephony/{provider}/`, use provider signature verification, return quickly after durable storage, and not use interactive-user authentication.

# Security

## Baseline

- Secrets are environment-managed and never use `NEXT_PUBLIC_` unless intentionally browser-visible.
- Production refuses debug mode and placeholder Django secrets.
- Session cookies are HttpOnly, Secure in production, and SameSite=Lax; unsafe requests require CSRF protection.
- Organization membership and role permissions are checked server-side for every tenant resource.
- Webhooks require provider signatures, replay prevention, idempotency, strict parsing, and request limits.
- Recordings use private object storage and short-lived signed URLs; application logs never contain recordings, credentials, authorization headers, or full sensitive payloads.
- Audit events record privileged actions and integration configuration changes.
- Dependencies, containers, and code are scanned in CI; supported runtime versions are pinned.

## Threat priorities

Primary risks are cross-tenant data access, forged/replayed webhooks, leaked call recordings, over-privileged integrations, spreadsheet/export leakage, and background tasks executing under the wrong tenant. Tests must include object-level authorization, tenant-filter bypass attempts, webhook replay, and task tenant-context validation.

Authentication is deliberately first-party session based in Phase 0. MFA/SSO can be added through an identity provider later. Password reset, lockout, and account recovery must be implemented before production access is broadened.

# Database Architecture

PostgreSQL is the system of record. Models use UUID keys, UTC timestamps, explicit foreign keys, and database constraints. Every tenant-owned aggregate includes a non-null `organization_id`; uniqueness is generally scoped to it. Deletion defaults to protection or soft lifecycle state for business/audit data, with retention jobs introduced only when policy is approved.

```mermaid
erDiagram
    ORGANIZATION ||--o{ MEMBERSHIP : has
    USER ||--o{ MEMBERSHIP : joins
    ORGANIZATION ||--o{ TEAM : owns
    TEAM ||--o{ AGENT_ASSIGNMENT : has
    USER ||--o{ AGENT_ASSIGNMENT : acts_as
    ORGANIZATION ||--o{ PHONE_NUMBER : owns
    ORGANIZATION ||--o{ CONTACT : owns
    ORGANIZATION ||--o{ CALL : owns
    PHONE_NUMBER ||--o{ CALL : handles
    CONTACT ||--o{ CALL : participates
    CALL ||--o{ CALL_EVENT : contains
    ORGANIZATION ||--o{ RAW_WEBHOOK_EVENT : receives
    ORGANIZATION ||--o{ LEAD : owns
    ORGANIZATION ||--o{ CAMPAIGN : owns
    ORGANIZATION ||--o{ FOLLOWUP : owns
    ORGANIZATION ||--o{ AUDIT_EVENT : records
```

## Tenant enforcement

The initial safeguard is defense in depth: organization-scoped managers/querysets, service methods requiring an organization context, serializer validation, permission classes, and tests proving cross-organization access fails. Background jobs carry organization IDs explicitly. PostgreSQL row-level security is a possible later hardening layer, not the only isolation mechanism and not enabled prematurely.

## Migration discipline

Each domain owns its migrations. Production changes are backward-compatible in staged deployments: add nullable/additive schema, deploy code, backfill asynchronously, enforce constraints, then remove obsolete schema in a later release. Analytics starts with indexed queries/materialized views where justified; a warehouse is deferred.

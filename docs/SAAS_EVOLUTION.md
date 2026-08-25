# SaaS Evolution

The initial company is represented as the first `Organization`, not as global implicit state. Users join through memberships; teams, agents, phone numbers, calls, contacts, workflows, analytics, integration credentials, and audit records are organization-owned.

Evolution is incremental:

1. Validate organization-scoped domain behavior with the single internal tenant.
2. Add organization selection, invitations, tenant administration, and automated isolation tests.
3. Add per-tenant configuration, quotas, retention, and operational tooling.
4. Harden isolation with PostgreSQL RLS if justified and move high-volume analytics to dedicated read infrastructure only when measurements demand it.
5. Add public onboarding, subscriptions, and billing as separate modules after product and compliance requirements are known.

No core model should assume one global company, provider, timezone, currency, or retention policy. Conversely, premature sharding, microservices, per-tenant databases, billing, and multi-workspace UI are intentionally excluded.

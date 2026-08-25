# Telephony Integration Architecture

Provider implementations satisfy a `TelephonyProvider` protocol responsible for signature verification, payload parsing, API calls, and provider identifier translation. Core `Call` and `CallEvent` models contain no provider-specific fields; external identifiers and raw payloads stay in telephony-owned records.

```mermaid
sequenceDiagram
    participant P as Telephony Provider
    participant W as Webhook Endpoint
    participant DB as PostgreSQL
    participant Q as Celery/Redis
    participant N as Normalizer
    participant C as Calls Domain
    P->>W: Signed webhook
    W->>W: Verify signature and limits
    W->>DB: Insert RawWebhookEvent (idempotent)
    W->>Q: Enqueue raw event ID
    W-->>P: 202 Accepted
    Q->>N: Process raw event
    N->>DB: Insert normalized CallEvent
    N->>C: Apply idempotent transition
    C->>DB: Update Call/workflow state
```

Secrets remain server-side. Verification uses the exact raw request body and constant-time comparison. Payload size, content type, timestamp tolerance, replay keys, rate limits, and provider IP guidance are enforced at ingress. A provider is selected by configuration and registry; adding one means adding an adapter and contract tests, not changing calls-domain behavior.

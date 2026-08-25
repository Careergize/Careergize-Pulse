from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Protocol


@dataclass(frozen=True)
class NormalizedEvent:
    provider_event_id: str
    event_type: str
    occurred_at: datetime
    external_call_id: str
    data: Mapping[str, Any]


class TelephonyProvider(Protocol):
    slug: str

    def verify_webhook(self, raw_body: bytes, headers: Mapping[str, str]) -> bool: ...

    def normalize_webhook(self, payload: Mapping[str, Any]) -> tuple[NormalizedEvent, ...]: ...

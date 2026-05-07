from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from domain.enums.event_category import EventCategory
from domain.enums.event_status import EventStatus


@dataclass(slots=True)
class Event:
    source_id: str
    event_type: str
    event_category: EventCategory
    occurred_at: datetime
    received_at: datetime
    processed_at: datetime | None
    processing_status: EventStatus
    payload: dict[str, Any]
    meta: dict[str, Any]
    error_message: str | None
    id: UUID = field(default_factory=uuid4)

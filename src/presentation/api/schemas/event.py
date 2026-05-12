from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, field_validator

from domain.enums.event_category import EventCategory
from domain.enums.event_status import EventStatus


class EventRequestSchema(BaseModel):
    event_type: str
    occurred_at: datetime
    payload: dict[str, Any]

    @field_validator("event_type")
    @classmethod
    def event_type_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("event_type must not be empty")
        return v


class EventSyncResponseSchema(BaseModel):
    id: UUID
    event_type: str
    event_category: EventCategory
    processing_status: EventStatus
    occurred_at: datetime
    received_at: datetime
    processed_at: datetime | None
    payload: dict[str, Any]
    meta: dict[str, Any]
    error_message: str | None = None

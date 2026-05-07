from datetime import datetime
from typing import Any

from pydantic import BaseModel, field_validator


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

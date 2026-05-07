from datetime import datetime
from typing import Any

from pydantic import BaseModel

from application.dto.event import IncomingEventDTO


class EventMessageSchema(BaseModel):
    event_type: str
    occurred_at: datetime
    payload: dict[str, Any]
    source_id: str
    received_at: datetime

    def to_dto(self) -> IncomingEventDTO:
        return IncomingEventDTO(
            event_type=self.event_type,
            occurred_at=self.occurred_at,
            payload=self.payload,
            source_id=self.source_id,
            received_at=self.received_at,
        )

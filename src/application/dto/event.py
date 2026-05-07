from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class IncomingEventDTO:
    event_type: str
    occurred_at: datetime
    payload: dict[str, Any]
    source_id: str
    received_at: datetime

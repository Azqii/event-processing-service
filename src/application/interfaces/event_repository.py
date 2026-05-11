from datetime import datetime
from typing import Protocol

from application.dto.analytics import EventCountBySourceDTO, EventCountByTypeDTO
from domain.entities.event import Event


class EventRepository(Protocol):
    async def save(self, event: Event) -> None: ...
    async def count_by_type(
        self, date_from: datetime, date_until: datetime
    ) -> list[EventCountByTypeDTO]: ...
    async def count_by_source(
        self, date_from: datetime, date_until: datetime
    ) -> list[EventCountBySourceDTO]: ...

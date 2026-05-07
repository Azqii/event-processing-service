from typing import Protocol

from application.dto.event import IncomingEventDTO


class EventPublisher(Protocol):
    async def publish(self, event: IncomingEventDTO) -> None: ...

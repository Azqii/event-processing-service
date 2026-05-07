from application.dto.event import IncomingEventDTO
from application.interfaces.event_publisher import EventPublisher


class AcceptEventUseCase:
    def __init__(self, publisher: EventPublisher) -> None:
        self._publisher = publisher

    async def execute(self, dto: IncomingEventDTO) -> None:
        await self._publisher.publish(dto)

from application.dto.event import IncomingEventDTO
from application.services.event_processing import (
    EventProcessingService,
)
from domain.entities.event import Event


class ProcessEventUseCase:
    def __init__(self, service: EventProcessingService) -> None:
        self._service = service

    async def execute(self, dto: IncomingEventDTO) -> Event:
        return await self._service.process(dto)

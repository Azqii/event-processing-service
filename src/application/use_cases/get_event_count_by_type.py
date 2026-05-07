from datetime import datetime

from application.dto.analytics import EventCountByTypeDTO
from application.exceptions import InvalidDateRangeError
from application.interfaces.event_repository import EventRepository


class GetEventCountByTypeUseCase:
    def __init__(self, repository: EventRepository) -> None:
        self._repository = repository

    async def count_by_type(
        self, date_from: datetime, date_until: datetime
    ) -> list[EventCountByTypeDTO]:
        if date_from >= date_until:
            raise InvalidDateRangeError(
                "date_from must be less than date_until"
            )
        return await self._repository.count_by_type(date_from, date_until)

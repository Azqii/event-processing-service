import json
import logging
from datetime import datetime

from clickhouse_connect.driver.asyncclient import AsyncClient

from application.dto.analytics import EventCountByTypeDTO
from application.exceptions import RepositoryError
from application.interfaces.event_repository import EventRepository
from domain.entities.event import Event

logger = logging.getLogger(__name__)


class ClickHouseEventRepository(EventRepository):
    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def save(self, event: Event) -> None:
        data = [
            [
                event.id,
                event.source_id,
                event.event_type,
                str(event.event_category),
                event.occurred_at,
                event.received_at,
                event.processed_at,
                str(event.processing_status),
                json.dumps(event.payload),
                json.dumps(event.meta),
                event.error_message,
            ]
        ]
        column_names = [
            "id",
            "source_id",
            "event_type",
            "event_category",
            "occurred_at",
            "received_at",
            "processed_at",
            "processing_status",
            "payload",
            "meta",
            "error_message",
        ]
        try:
            await self._client.insert(
                "events", data, column_names=column_names
            )
        except Exception as exc:
            raise RepositoryError(f"Failed to save event: {exc}") from exc

    async def count_by_type(
        self, date_from: datetime, date_until: datetime
    ) -> list[EventCountByTypeDTO]:
        query = """
            SELECT event_type, count() AS count
            FROM events
            WHERE occurred_at >= {date_from:DateTime}
              AND occurred_at < {date_until:DateTime}
            GROUP BY event_type
            ORDER BY count DESC
        """
        try:
            result = await self._client.query(
                query,
                parameters={"date_from": date_from, "date_until": date_until},
            )
        except Exception as exc:
            raise RepositoryError(f"Failed to query events: {exc}") from exc
        return [
            EventCountByTypeDTO(event_type=row[0], count=row[1])
            for row in result.result_rows
        ]

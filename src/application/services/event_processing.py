import json
import logging
from datetime import datetime
from typing import Any

from application.dto.event import IncomingEventDTO
from application.exceptions import EventProcessingError
from application.interfaces.event_repository import EventRepository
from domain.entities.event import Event
from domain.enums.event_status import EventStatus
from domain.services.event_category_resolver import resolve_event_category
from shared.time import utc_now

logger = logging.getLogger(__name__)

class EventProcessingService:
    _LATE_THRESHOLD_MS = 60_000
    _REQUIRED_PAYLOAD_FIELDS: dict[str, set[str]] = {
        "user.login": {"user_id"},
        "user.logout": {"user_id"},
        "user.registered": {"user_id"},
        "page.viewed": {"page_url"},
        "system.error": {"message"},
    }

    def __init__(
        self, repository: EventRepository, handler_version: str
    ) -> None:
        self._repository = repository
        self._handler_version = handler_version

    async def process(self, dto: IncomingEventDTO) -> Event:
        processing_started_at = utc_now()
        normalized_type = dto.event_type.strip().lower()
        event_category = resolve_event_category(normalized_type)

        status = EventStatus.PROCESSED
        error_message: str | None = None

        try:
            self._validate_payload(normalized_type, dto.payload)
        except EventProcessingError as exc:
            status = EventStatus.FAILED
            error_message = str(exc)
            logger.warning(
                "Payload validation failed: event_type=%s error=%s",
                normalized_type,
                error_message,
            )

        processed_at = utc_now()
        event = Event(
            source_id=dto.source_id,
            event_type=normalized_type,
            event_category=event_category,
            occurred_at=dto.occurred_at,
            received_at=dto.received_at,
            processed_at=processed_at,
            processing_status=status,
            payload=dto.payload,
            meta=self._build_meta(dto, processing_started_at, processed_at),
            error_message=error_message,
        )

        try:
            await self._repository.save(event)
        except Exception as exc:
            logger.error(
                "Failed to save event: id=%s event_type=%s error=%s",
                event.id,
                event.event_type,
                exc,
            )
            raise

        return event

    def _validate_payload(
        self, event_type: str, payload: dict[str, Any]
    ) -> None:
        required = self._REQUIRED_PAYLOAD_FIELDS.get(event_type)
        if required is None:
            return
        missing = sorted(required - payload.keys())
        if missing:
            raise EventProcessingError(
                f"Missing required payload fields: {', '.join(missing)}"
            )

    def _build_meta(
        self,
        dto: IncomingEventDTO,
        processing_started_at: datetime,
        processed_at: datetime,
    ) -> dict[str, Any]:
        delivery_delay_ms = int(
            (dto.received_at - dto.occurred_at).total_seconds() * 1000
        )
        return {
            "delivery_delay_ms": delivery_delay_ms,
            "processing_time_ms": round(
                (processed_at - processing_started_at).total_seconds() * 1000,
                3,
            ),
            "handler_version": self._handler_version,
            "is_late": delivery_delay_ms > self._LATE_THRESHOLD_MS,
            "payload_size": len(
                json.dumps(dto.payload, ensure_ascii=False)
            ),
        }

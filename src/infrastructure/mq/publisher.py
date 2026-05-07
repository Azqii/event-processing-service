from faststream.kafka import KafkaBroker

from application.dto.event import IncomingEventDTO
from application.exceptions import PublisherError
from application.interfaces.event_publisher import EventPublisher
from infrastructure.config.kafka import KafkaSettings


class KafkaEventPublisher(EventPublisher):
    def __init__(
        self, broker: KafkaBroker, settings: KafkaSettings
    ) -> None:
        self._broker = broker
        self._topic = settings.KAFKA_EVENTS_TOPIC

    async def publish(self, event: IncomingEventDTO) -> None:
        message = {
            "event_type": event.event_type,
            "occurred_at": event.occurred_at.isoformat(),
            "payload": event.payload,
            "source_id": event.source_id,
            "received_at": event.received_at.isoformat(),
        }
        try:
            await self._broker.publish(message, topic=self._topic)
        except Exception as exc:
            raise PublisherError(
                f"Failed to publish event to Kafka: {exc}"
            ) from exc

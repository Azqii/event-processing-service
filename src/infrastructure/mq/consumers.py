import logging

from dishka.integrations.faststream import FromDishka as Depends
from dishka.integrations.faststream import inject
from faststream.kafka import KafkaRoute, KafkaRouter

from application.use_cases.process_event import ProcessEventUseCase
from infrastructure.config.kafka import KafkaSettings
from infrastructure.mq.schemas import EventMessageSchema

logger = logging.getLogger(__name__)

settings = KafkaSettings()


@inject
async def handle_event(
    data: EventMessageSchema,
    use_case: Depends[ProcessEventUseCase],
) -> None:
    await use_case.execute(data.to_dto())


router = KafkaRouter(
    handlers=[
        KafkaRoute(handle_event, settings.KAFKA_EVENTS_TOPIC),
    ]
)

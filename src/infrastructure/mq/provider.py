from faststream.kafka import KafkaBroker
from faststream.security import SASLPlaintext

from infrastructure.config.kafka import KafkaSettings


def create_kafka_broker(settings: KafkaSettings) -> KafkaBroker:
    security = SASLPlaintext(
        username=settings.KAFKA_SASL_USERNAME,
        password=settings.KAFKA_SASL_PASSWORD,
    )
    return KafkaBroker(settings.KAFKA_BOOTSTRAP_SERVERS, security=security)

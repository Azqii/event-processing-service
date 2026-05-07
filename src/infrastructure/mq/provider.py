from faststream.kafka import KafkaBroker

from infrastructure.config.kafka import KafkaSettings


def create_kafka_broker(settings: KafkaSettings) -> KafkaBroker:
    return KafkaBroker(settings.KAFKA_BOOTSTRAP_SERVERS)

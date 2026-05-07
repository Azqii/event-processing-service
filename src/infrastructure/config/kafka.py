from infrastructure.config.base import BaseConfig


class KafkaSettings(BaseConfig):
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_EVENTS_TOPIC: str = "events"

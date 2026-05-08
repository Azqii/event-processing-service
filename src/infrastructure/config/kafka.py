from infrastructure.config.base import BaseConfig


class KafkaSettings(BaseConfig):
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"
    KAFKA_EVENTS_TOPIC: str = "events"
    KAFKA_SASL_USERNAME: str = "admin"
    KAFKA_SASL_PASSWORD: str = "admin"

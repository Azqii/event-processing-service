from dishka.integrations.faststream import setup_dishka
from faststream import FastStream

from infrastructure.config.kafka import KafkaSettings
from infrastructure.di.container import create_container
from infrastructure.mq import consumers
from infrastructure.mq.provider import create_kafka_broker

settings = KafkaSettings()
container = create_container()

broker = create_kafka_broker(settings)
broker.include_router(consumers.router)

app = FastStream(broker)

setup_dishka(container, app)

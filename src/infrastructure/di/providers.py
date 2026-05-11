from collections.abc import AsyncIterator

from clickhouse_connect.driver.asyncclient import AsyncClient
from dishka import Provider, Scope, provide
from faststream.kafka import KafkaBroker

from application.interfaces.event_publisher import EventPublisher
from application.interfaces.event_repository import EventRepository
from application.interfaces.token_verifier import TokenVerifier
from application.services.event_processing import (
    EventProcessingService,
)
from application.use_cases.accept_event import AcceptEventUseCase
from application.use_cases.get_event_count_by_source import (
    GetEventCountBySourceUseCase,
)
from application.use_cases.get_event_count_by_type import (
    GetEventCountByTypeUseCase,
)
from application.use_cases.process_event import ProcessEventUseCase
from infrastructure.auth.jwks_client import JWKSClient
from infrastructure.auth.keycloak_token_verifier import KeycloakTokenVerifier
from infrastructure.config.app import AppSettings
from infrastructure.config.clickhouse import ClickHouseSettings
from infrastructure.config.kafka import KafkaSettings
from infrastructure.config.keycloak import KeycloakSettings
from infrastructure.mq.provider import create_kafka_broker
from infrastructure.mq.publisher import KafkaEventPublisher
from infrastructure.olap.client import create_clickhouse_client
from infrastructure.olap.repository import ClickHouseEventRepository


class AppProvider(Provider):
    @provide(scope=Scope.APP)
    def get_app_settings(self) -> AppSettings:
        return AppSettings()

    @provide(scope=Scope.APP)
    def get_kafka_settings(self) -> KafkaSettings:
        return KafkaSettings()

    @provide(scope=Scope.APP)
    def get_clickhouse_settings(self) -> ClickHouseSettings:
        return ClickHouseSettings()

    @provide(scope=Scope.APP)
    def get_keycloak_settings(self) -> KeycloakSettings:
        return KeycloakSettings()

    @provide(scope=Scope.APP)
    def get_jwks_client(self, settings: KeycloakSettings) -> JWKSClient:
        return JWKSClient(settings.KEYCLOAK_JWKS_URL)

    @provide(scope=Scope.APP)
    def get_token_verifier(
        self,
        settings: KeycloakSettings,
        jwks_client: JWKSClient,
    ) -> TokenVerifier:
        return KeycloakTokenVerifier(settings, jwks_client)

    @provide(scope=Scope.APP)
    async def get_kafka_broker(
        self, settings: KafkaSettings
    ) -> AsyncIterator[KafkaBroker]:
        broker = create_kafka_broker(settings)
        await broker.start()
        yield broker
        await broker.close()

    @provide(scope=Scope.APP)
    async def get_clickhouse_client(
        self, settings: ClickHouseSettings
    ) -> AsyncClient:
        return await create_clickhouse_client(settings)

    @provide(scope=Scope.APP)
    def get_event_repository(self, client: AsyncClient) -> EventRepository:
        return ClickHouseEventRepository(client)

    @provide(scope=Scope.APP)
    def get_event_publisher(
        self, broker: KafkaBroker, settings: KafkaSettings
    ) -> EventPublisher:
        return KafkaEventPublisher(broker, settings)

    @provide(scope=Scope.APP)
    def get_event_processing_service(
        self,
        repository: EventRepository,
        settings: AppSettings,
    ) -> EventProcessingService:
        return EventProcessingService(
            repository, settings.EVENT_HANDLER_VERSION
        )

    @provide(scope=Scope.REQUEST)
    def get_accept_event_use_case(
        self, publisher: EventPublisher
    ) -> AcceptEventUseCase:
        return AcceptEventUseCase(publisher)

    @provide(scope=Scope.REQUEST)
    def get_process_event_use_case(
        self, service: EventProcessingService
    ) -> ProcessEventUseCase:
        return ProcessEventUseCase(service)

    @provide(scope=Scope.REQUEST)
    def get_event_count_by_type_use_case(
        self, repository: EventRepository
    ) -> GetEventCountByTypeUseCase:
        return GetEventCountByTypeUseCase(repository)

    @provide(scope=Scope.REQUEST)
    def get_event_count_by_source_use_case(
        self, repository: EventRepository
    ) -> GetEventCountBySourceUseCase:
        return GetEventCountBySourceUseCase(repository)

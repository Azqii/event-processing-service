from infrastructure.config.base import BaseConfig


class ClickHouseSettings(BaseConfig):
    CLICKHOUSE_HOST: str = "clickhouse"
    CLICKHOUSE_PORT: int = 8123
    CLICKHOUSE_USER: str = "admin"
    CLICKHOUSE_PASSWORD: str = "admin"
    CLICKHOUSE_DATABASE: str = "events"

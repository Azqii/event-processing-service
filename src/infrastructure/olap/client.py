import clickhouse_connect
from clickhouse_connect.driver.asyncclient import AsyncClient

from infrastructure.config.clickhouse import ClickHouseSettings


async def create_clickhouse_client(
    settings: ClickHouseSettings,
) -> AsyncClient:
    return await clickhouse_connect.get_async_client(
        host=settings.CLICKHOUSE_HOST,
        port=settings.CLICKHOUSE_PORT,
        username=settings.CLICKHOUSE_USER,
        password=settings.CLICKHOUSE_PASSWORD,
        database=settings.CLICKHOUSE_DATABASE,
    )

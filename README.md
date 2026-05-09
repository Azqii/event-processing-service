# event-processing-service

Event processing service built with FastAPI, FastStream, Kafka and ClickHouse.

## Запуск

```bash
# Инфраструктура (Kafka, ClickHouse, Keycloak)
docker compose -f infra-docker-compose.yml up -d

# Приложение
docker compose up -d
```

Конфигурация — `.env` (пример в `.env.example`).

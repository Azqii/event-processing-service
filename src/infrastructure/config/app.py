from infrastructure.config.base import BaseConfig


class AppSettings(BaseConfig):
    APP_NAME: str = "event-processing-service"
    APP_VERSION: str = "0.1.0"
    EVENT_HANDLER_VERSION: str = "1.0.0"

from infrastructure.config.base import BaseConfig


class KeycloakSettings(BaseConfig):
    KEYCLOAK_ISSUER_URL: str = "http://localhost:8080/realms/event-processing"
    KEYCLOAK_JWKS_URL: str = "http://localhost:8080/realms/event-processing/protocol/openid-connect/certs"
    KEYCLOAK_AUDIENCE: str = "event-processing-api"
    KEYCLOAK_VERIFY_AUDIENCE: bool = False

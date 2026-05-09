import logging
from typing import Any

import jwt
from jwt import InvalidTokenError

from application.dto.auth import AuthenticatedClient
from application.exceptions import AuthenticationError
from infrastructure.auth.jwks_client import JWKSClient
from infrastructure.config.keycloak import KeycloakSettings

logger = logging.getLogger(__name__)

_ALGORITHMS = ["RS256", "RS384", "RS512", "ES256", "ES384", "ES512"]


class KeycloakTokenVerifier:
    def __init__(
        self,
        settings: KeycloakSettings,
        jwks_client: JWKSClient,
    ) -> None:
        self._settings = settings
        self._jwks_client = jwks_client

    async def verify(self, token: str) -> AuthenticatedClient:
        try:
            unverified_header = jwt.get_unverified_header(token)
        except InvalidTokenError as exc:
            raise AuthenticationError("Invalid token header") from exc

        kid: str | None = unverified_header.get("kid")
        if not kid:
            raise AuthenticationError("Token header missing kid claim")

        signing_key = await self._jwks_client.get_signing_key(kid)

        decode_options: dict[str, Any] = {
            "verify_aud": self._settings.KEYCLOAK_VERIFY_AUDIENCE,
        }
        decode_kwargs: dict[str, Any] = {
            "key": signing_key.key,
            "algorithms": _ALGORITHMS,
            "issuer": self._settings.KEYCLOAK_ISSUER_URL,
            "options": decode_options,
        }
        if self._settings.KEYCLOAK_VERIFY_AUDIENCE:
            decode_kwargs["audience"] = self._settings.KEYCLOAK_AUDIENCE

        try:
            claims: dict[str, Any] = jwt.decode(token, **decode_kwargs)
        except InvalidTokenError as exc:
            raise AuthenticationError("Token verification failed") from exc

        return self._build_authenticated_client(claims)

    def _build_authenticated_client(
        self, claims: dict[str, Any]
    ) -> AuthenticatedClient:
        source_id: str | None = (
            claims.get("azp")
            or claims.get("client_id")
            or claims.get("preferred_username")
            or claims.get("sub")
        )
        if not source_id:
            raise AuthenticationError(
                "Cannot determine source_id: no azp/client_id/"
                "preferred_username/sub claim"
            )

        roles: set[str] = set()
        realm_access = claims.get("realm_access", {})
        if isinstance(realm_access, dict):
            roles.update(realm_access.get("roles", []))

        return AuthenticatedClient(
            source_id=source_id,
            subject=claims.get("sub"),
            roles=roles,
        )

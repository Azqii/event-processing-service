from typing import Protocol

from application.dto.auth import AuthenticatedClient


class TokenVerifier(Protocol):
    async def verify(self, token: str) -> AuthenticatedClient: ...

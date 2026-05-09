import asyncio
import logging
from typing import Any

import httpx
from jwt import PyJWK

from application.exceptions import AuthenticationError

logger = logging.getLogger(__name__)


class JWKSClient:
    def __init__(self, jwks_url: str) -> None:
        self._jwks_url = jwks_url
        self._keys: dict[str, PyJWK] = {}
        self._lock = asyncio.Lock()

    async def get_signing_key(self, kid: str) -> PyJWK:
        if kid not in self._keys:
            await self._refresh_keys()
        if kid not in self._keys:
            raise AuthenticationError(f"Signing key not found for kid: {kid}")
        return self._keys[kid]

    async def _refresh_keys(self) -> None:
        async with self._lock:
            try:
                async with httpx.AsyncClient() as http_client:
                    response = await http_client.get(
                        self._jwks_url, timeout=10.0
                    )
                    response.raise_for_status()
                    jwks_data: dict[str, Any] = response.json()
            except httpx.HTTPError as exc:
                raise AuthenticationError(
                    f"Failed to fetch JWKS from {self._jwks_url}: {exc}"
                ) from exc

            new_keys: dict[str, PyJWK] = {}
            for key_data in jwks_data.get("keys", []):
                kid = key_data.get("kid", "")
                if not kid:
                    continue
                try:
                    new_keys[kid] = PyJWK(key_data)
                except Exception as exc:
                    logger.warning("Failed to parse JWK kid=%s: %s", kid, exc)

            self._keys = new_keys

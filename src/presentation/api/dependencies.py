import logging
from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import Depends, HTTPException, Request, status

from application.dto.auth import AuthenticatedClient
from application.exceptions import AuthenticationError
from application.interfaces.token_verifier import TokenVerifier

logger = logging.getLogger(__name__)


def _extract_bearer_token(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    if not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    return auth_header.removeprefix("Bearer ")


@inject
async def get_authenticated_client(
    request: Request,
    verifier: FromDishka[TokenVerifier],
) -> AuthenticatedClient:
    token = _extract_bearer_token(request)
    try:
        return await verifier.verify(token)
    except AuthenticationError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        ) from exc


async def require_admin(
    client: Annotated[AuthenticatedClient, Depends(get_authenticated_client)],
) -> AuthenticatedClient:
    if "admin" not in client.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )
    return client

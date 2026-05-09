from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, Response, status

from application.dto.auth import AuthenticatedClient
from application.dto.event import IncomingEventDTO
from application.use_cases.accept_event import AcceptEventUseCase
from presentation.api.dependencies import get_authenticated_client
from presentation.api.schemas.event import EventRequestSchema
from shared.time import utc_now

router = APIRouter(
    route_class=DishkaRoute,
    responses={401: {"description": "Unauthorized"}},
)


@router.post("", status_code=status.HTTP_202_ACCEPTED)
async def accept_event(
    body: EventRequestSchema,
    authenticated_client: Annotated[
        AuthenticatedClient, Depends(get_authenticated_client)
    ],
    use_case: FromDishka[AcceptEventUseCase],
) -> Response:
    dto = IncomingEventDTO(
        event_type=body.event_type,
        occurred_at=body.occurred_at,
        payload=body.payload,
        source_id=authenticated_client.source_id,
        received_at=utc_now(),
    )
    await use_case.execute(dto)
    return Response(status_code=status.HTTP_202_ACCEPTED)

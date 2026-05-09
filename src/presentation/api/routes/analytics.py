from datetime import datetime
from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, HTTPException

from application.dto.auth import AuthenticatedClient
from application.exceptions import InvalidDateRangeError
from application.use_cases.get_event_count_by_type import (
    GetEventCountByTypeUseCase,
)
from presentation.api.dependencies import require_admin
from presentation.api.schemas.analytics import EventCountByTypeResponseSchema

router = APIRouter(
    route_class=DishkaRoute,
    responses={
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
    },
)


@router.get(
    "/events/count-by-type",
    response_model=list[EventCountByTypeResponseSchema],
)
async def get_event_count_by_type(
    date_from: datetime,
    date_until: datetime,
    _auth: Annotated[AuthenticatedClient, Depends(require_admin)],
    use_case: FromDishka[GetEventCountByTypeUseCase],
) -> list[EventCountByTypeResponseSchema]:
    try:
        results = await use_case.count_by_type(date_from, date_until)
    except InvalidDateRangeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return [
        EventCountByTypeResponseSchema(event_type=r.event_type, count=r.count)
        for r in results
    ]

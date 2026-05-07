from datetime import datetime

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException

from application.exceptions import InvalidDateRangeError
from application.use_cases.get_event_count_by_type import (
    GetEventCountByTypeUseCase,
)
from presentation.api.schemas.analytics import EventCountByTypeResponseSchema

router = APIRouter(route_class=DishkaRoute)


@router.get(
    "/events/count-by-type",
    response_model=list[EventCountByTypeResponseSchema],
)
async def get_event_count_by_type(
    date_from: datetime,
    date_until: datetime,
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

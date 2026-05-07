from fastapi import APIRouter

from presentation.api.routes import analytics, events

router = APIRouter(prefix="/api/v1")

router.include_router(events.router, prefix="/events", tags=["events"])
router.include_router(
    analytics.router, prefix="/analytics", tags=["analytics"]
)

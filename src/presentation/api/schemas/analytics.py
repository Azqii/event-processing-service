from pydantic import BaseModel


class EventCountByTypeResponseSchema(BaseModel):
    event_type: str
    count: int


class EventCountBySourceResponseSchema(BaseModel):
    source_id: str
    count: int

from pydantic import BaseModel


class EventCountByTypeResponseSchema(BaseModel):
    event_type: str
    count: int

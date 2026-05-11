from dataclasses import dataclass


@dataclass
class EventCountByTypeDTO:
    event_type: str
    count: int


@dataclass
class EventCountBySourceDTO:
    source_id: str
    count: int

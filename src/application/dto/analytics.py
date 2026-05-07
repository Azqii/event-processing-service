from dataclasses import dataclass


@dataclass
class EventCountByTypeDTO:
    event_type: str
    count: int

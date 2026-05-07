from enum import StrEnum


class EventCategory(StrEnum):
    AUTH = "AUTH"
    ACTIVITY = "ACTIVITY"
    SYSTEM = "SYSTEM"
    UNKNOWN = "UNKNOWN"

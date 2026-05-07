from domain.enums.event_category import EventCategory


def resolve_event_category(event_type: str) -> EventCategory:
    if event_type.startswith("user."):
        return EventCategory.AUTH
    if event_type.startswith("page."):
        return EventCategory.ACTIVITY
    if event_type.startswith("system."):
        return EventCategory.SYSTEM
    return EventCategory.UNKNOWN

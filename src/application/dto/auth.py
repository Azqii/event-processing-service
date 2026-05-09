from dataclasses import dataclass


@dataclass
class AuthenticatedClient:
    source_id: str
    subject: str | None
    roles: set[str]

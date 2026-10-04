import uuid
from dataclasses import dataclass

from inara.domain.commander import Commander


@dataclass(frozen=True)
class User:
    id: uuid.UUID
    login: str
    email: str
    password: str
    commander: Commander

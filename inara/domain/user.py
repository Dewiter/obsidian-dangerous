import uuid
from dataclasses import dataclass
from datetime import datetime

from inara.domain.commander import Commander


@dataclass(frozen=True)
class FrontierAccount:
    frontier_id: int  # Frontier's customer id, stable across logins
    access_token: str
    refresh_token: str
    expires_at: datetime


@dataclass(frozen=True)
class User:
    id: uuid.UUID
    login: str
    email: str
    password_hash: str
    # commander: Commander
    frontier: FrontierAccount | None = None

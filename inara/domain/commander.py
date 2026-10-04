import uuid
from dataclasses import dataclass

from inara.domain.ship import Ship


@dataclass(frozen=True)
class Commander:
    id: uuid.UUID
    frontier_id: int
    name: str
    fleet: list[Ship]

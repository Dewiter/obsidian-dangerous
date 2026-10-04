import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class Ship:
    id: uuid.UUID
    model: str
    brand: str
    location: str
    rebuy_cost: int
    outfit: dict
    current: bool

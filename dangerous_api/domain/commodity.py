from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CommodityPrice:
    market_id: int
    station: str
    system: str
    name: str
    buy_price: int
    sell_price: int
    stock: int
    demand: int
    updated_at: datetime

from dangerous_api.domain.commodity import CommodityPrice


class InMemoryCommodityRepository:
    def __init__(self):
        self._prices: dict[tuple[int, str], CommodityPrice] = {}

    async def add_many(self, prices: list[CommodityPrice]) -> None:
        for p in prices:
            self._prices[(p.market_id, p.station)] = p

    async def list_by_name(self, name: str) -> list[CommodityPrice]:
        return [p for p in self._prices.values() if p.name == name]

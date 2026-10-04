from typing import Protocol

from dangerous_api.domain.commodity import CommodityPrice


class CommodityRepository(Protocol):
    async def add_many(self, prices: list[CommodityPrice]) -> None: ...
    async def list_by_name(self, name: str) -> list[CommodityPrice]: ...


class CommodityService:
    def __init__(self, repo: CommodityRepository):
        self.repo = repo

    async def record_market(self, prices: list[CommodityPrice]) -> None:
        # business rules go here (skip zero-price items, reject stale data, etc.)
        if prices:
            await self.repo.add_many(prices)

    async def best_sell_locations(self, name: str) -> list[CommodityPrice]:
        prices = await self.repo.list_by_name(name)
        return sorted(prices, key=lambda p: p.sell_price, reverse=True)[:10]

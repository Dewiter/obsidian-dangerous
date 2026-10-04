from functools import lru_cache

from dangerous_api.service.commodity import CommodityService
from dangerous_api.storage.memory.commodity import InMemoryCommodityRepository


@lru_cache
def commodity_service() -> CommodityService:
    return CommodityService(InMemoryCommodityRepository())

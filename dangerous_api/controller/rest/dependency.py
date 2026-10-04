from typing import Annotated

from fastapi import Depends

from dangerous_api.bootstrap.container import commodity_service
from dangerous_api.service.commodity import CommodityService


def get_commodity_service() -> CommodityService:
    return commodity_service()


CommodityServiceDep = Annotated[CommodityService, Depends(get_commodity_service)]

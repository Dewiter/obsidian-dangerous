from typing import Annotated

from fastapi import Depends

from inara.bootstrap.container import commodity_service
from inara.service.commodity import CommodityService


def get_commodity_service() -> CommodityService:
    return commodity_service()


CommodityServiceDep = Annotated[CommodityService, Depends(get_commodity_service)]

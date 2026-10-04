from datetime import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict

from dangerous_api.controller.rest.dependency import CommodityServiceDep

router = APIRouter(prefix="/commodities", tags=["commodities"])


class PriceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    station: str
    system: str
    sell_price: str
    demand: int
    updated_at: datetime


@router.get("/{name}/best-sell", response_model=list[PriceOut])
async def best_sell(name: str, svc: CommodityServiceDep):
    prices = await svc.best_sell_locations(name.lower())
    if not prices:
        raise HTTPException(status_code=404, detail=f"No data for '{name}'")
    return prices

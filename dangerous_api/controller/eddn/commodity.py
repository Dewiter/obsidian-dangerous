import logging
from collections.abc import AsyncIterable
from datetime import datetime

from dangerous_api.domain.commodity import CommodityPrice
from dangerous_api.service.commodity import CommodityService

log = logging.getLogger(__name__)

COMMODITY_SCHEMA_REF = "https://eddn.edcd.io/schemas/commodity"


def is_commodity(data: dict) -> bool:
    return data.get("$schemaRef", "").startswith(COMMODITY_SCHEMA_REF)


def parse_commodity(data: dict) -> list[CommodityPrice]:
    msg = data["message"]
    updated_at = datetime.fromisoformat(msg["timestamp"])
    return [
        CommodityPrice(
            updated_at=updated_at,
            market_id=msg["marketID"],
            station=msg["station"],
            system=msg["system"],
            name=msg["name"],
            buy_price=msg["buyPrice"],
            sell_price=msg["sellPrice"],
            stock=msg["stock"],
            demand=msg["demand"],
        )
        for c in msg["commodities"]
    ]


async def run(service: CommodityService, messages: AsyncIterable) -> None:
    """Consumes EDDN envolopes and feed commodity ones tot the service.

    `messages` is injected, so tests can pass a fake async generator.
    """
    async for data in messages:
        if not is_commodity(data):
            continue
        try:
            prices = parse_commodity(data)
        except (KeyError, ValueError) as error:
            log.warning("Skipping malformed commodity message: %r", error)
            continue
        await service.record_market(prices)
        log.debug("Recorded: %d", len(prices))

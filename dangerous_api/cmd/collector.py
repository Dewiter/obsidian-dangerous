import asyncio

from dangerous_api.bootstrap.container import commodity_service
from dangerous_api.client import eddn
from dangerous_api.configs.setting import settings
from dangerous_api.controller.eddn.commodity import run
from dangerous_api.pkg.logging import setup_logging


def main() -> None:
    setup_logging(settings.log_level)
    asyncio.run(run(commodity_service(), eddn.messages(settings.eddn_url)))


if __name__ == "__main__":
    main()

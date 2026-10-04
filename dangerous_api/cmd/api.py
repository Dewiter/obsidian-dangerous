import asyncio
from contextlib import asynccontextmanager, suppress

from fastapi import FastAPI

from dangerous_api.bootstrap.container import commodity_service
from dangerous_api.client import eddn
from dangerous_api.configs.setting import settings
from dangerous_api.controller.eddn.commodity import run as run_collector
from dangerous_api.controller.rest.router import api_router
from dangerous_api.pkg.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = None
    if settings.embed_collector:
        task = asyncio.create_task(
            run_collector(commodity_service(), eddn.messages(settings.eddn_url))
        )
    yield
    if task:
        task.cancel()
        with suppress(asyncio.CancelledError):
            await task


def create_app() -> FastAPI:
    setup_logging(settings.log_level)
    app = FastAPI(title="Dangerous API", lifespan=lifespan)
    app.include_router(api_router)
    return app


app = create_app()

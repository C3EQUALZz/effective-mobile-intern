from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi
from fastapi import FastAPI
from redis.asyncio import (
    ConnectionPool,
    Redis,
)
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import clear_mappers

from app.application.api.trading_result import trading_result_router
from app.application.jobs import base
from app.application.utils.cache import cache
from app.infrastructure.adapters.alchemy.metadata import metadata
from app.infrastructure.adapters.alchemy.orm import start_mappers
from app.logic.container import container


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    if not base.broker.is_worker_process:
        await base.broker.startup()

    engine: AsyncEngine = await container.get(AsyncEngine)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    cache.pool = await container.get(ConnectionPool)
    cache.client = await container.get(Redis)

    start_mappers()

    yield

    if not base.broker.is_worker_process:
        await base.broker.shutdown()

    await app.state.dishka_container.close()
    clear_mappers()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Backend for Parser",
        description="Backend API written with FastAPI for parsing",
        root_path="/api",
        debug=True,
        lifespan=lifespan,
    )

    setup_dishka_fastapi(container=container, app=app)

    app.include_router(trading_result_router)

    return app
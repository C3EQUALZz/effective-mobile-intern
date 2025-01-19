import asyncio

from faststream import FastStream
from faststream.kafka import KafkaBroker
from sqlalchemy.ext.asyncio import AsyncEngine
from dishka.integrations.faststream import setup_dishka
from app.infrastructure.adapters.alchemy.metadata import metadata
from app.infrastructure.adapters.alchemy.orm import start_mappers
from app.logic.container import container
from app.application.consumers.trading_result.handlers import router as trading_result_router


async def main() -> None:
    broker: KafkaBroker = await container.get(KafkaBroker)

    setup_dishka(container=container, app=FastStream(broker=broker))

    engine: AsyncEngine = await container.get(AsyncEngine)

    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    start_mappers()

    broker.include_router(trading_result_router)


if __name__ == '__main__':
    asyncio.run(main())

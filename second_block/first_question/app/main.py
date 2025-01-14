import asyncio

from app.infrastructure.adapters.alchemy.orm import start_mappers
from app.infrastructure.container import get_container
from sqlalchemy.ext.asyncio import AsyncEngine
from app.infrastructure.adapters.alchemy.metadata import metadata
from sqlalchemy.orm import clear_mappers


async def main() -> None:
    container = get_container()

    engine: AsyncEngine = container.resolve(AsyncEngine)

    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    start_mappers()

    # clear_mappers()


if __name__ == '__main__':
    asyncio.run(main())

from typing import AsyncGenerator, Generator

import pytest
from sqlalchemy.exc import ArgumentError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncConnection
from testcontainers.postgres import PostgresContainer

from app.infrastructure.adapters.alchemy.metadata import metadata
from app.infrastructure.adapters.alchemy.orm import start_mappers


@pytest.fixture(scope="session")
def postgres_container() -> Generator[PostgresContainer]:
    with PostgresContainer("postgres:16") as postgres:
        yield postgres


@pytest.fixture
async def async_connection(postgres_container: PostgresContainer) -> AsyncGenerator[AsyncConnection, None]:
    uri = postgres_container.get_connection_url().replace("postgresql://", "postgresql+asyncpg://")
    engine: AsyncEngine = create_async_engine(uri)

    async with engine.begin() as conn:
        yield conn


@pytest.fixture
async def create_test_db(async_connection: AsyncConnection) -> AsyncGenerator[None, None]:
    await async_connection.run_sync(metadata.create_all)
    yield
    await async_connection.run_sync(metadata.drop_all)


@pytest.fixture
async def map_models_to_orm(create_test_db: None) -> None:
    """
    Create mappings from models to ORM according to DDD.
    """

    try:
        start_mappers()
    except ArgumentError:
        pass


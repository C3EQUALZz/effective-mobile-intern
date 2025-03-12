from typing import AsyncGenerator, Any

import pytest
from sqlalchemy import insert
from sqlalchemy.exc import ArgumentError, IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncConnection

from app.domain.entities.trading_result import TradingResultEntity
from app.infrastructure.adapters.alchemy.orm import metadata
from app.infrastructure.adapters.alchemy.orm import start_mappers
from tests.unit_test.test_infrastructure.utils import FakeTradingResultConfig


@pytest.fixture(scope="session")
async def async_engine() -> AsyncGenerator[AsyncEngine, Any]:
    """Фикстура для создания единственного движка на всю сессию тестов"""
    engine = create_async_engine(
        "sqlite+aiosqlite:///file:memdb?mode=memory&cache=shared&uri=true",
        echo=False
    )
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
async def async_connection(async_engine: AsyncEngine) -> AsyncGenerator[AsyncConnection, None]:
    async with async_engine.begin() as conn:
        yield conn


@pytest.fixture(scope="session")
async def create_test_db(async_connection: AsyncConnection) -> AsyncGenerator[None, None]:
    await async_connection.run_sync(metadata.create_all)
    yield
    await async_connection.run_sync(metadata.drop_all)


@pytest.fixture(scope="session")
async def map_models_to_orm(create_test_db: None) -> None:
    """
    Create mappings from models to ORM according to DDD.
    """

    try:
        start_mappers()

    except ArgumentError:
        pass


@pytest.fixture(scope="session")
async def create_test_user(
        map_models_to_orm: None,
        async_engine: AsyncEngine
) -> None:
    """
    Creates test user in test database, if user with provided credentials does not exist.
    """
    test_user_config = FakeTradingResultConfig()

    async with async_engine.begin() as conn:
        try:
            result = await conn.execute(
                insert(TradingResultEntity).values(**test_user_config.to_dict(to_lower=True))
            )
            assert result.rowcount == 1
        except IntegrityError:
            await conn.rollback()
            raise

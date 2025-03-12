from typing import Optional

import pytest
from sqlalchemy.ext.asyncio import AsyncConnection, async_sessionmaker, AsyncSession

from app.domain.entities.trading_result import TradingResultEntity
from app.infrastructure.repositories.trading_result.alchemy import SQLAlchemyTradingResultRepository
from tests.unit_test.test_infrastructure.utils import FakeTradingResultConfig


@pytest.mark.asyncio
async def test_sqlalchemy_trading_result_repository_get_success(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:
    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    trading_result: Optional[TradingResultEntity] = await SQLAlchemyTradingResultRepository(session=session).get(oid="0866a2c2-a9fe-4f45-885b-11c4e3d2b102")

    assert trading_result is not None
    assert trading_result.oid == "0866a2c2-a9fe-4f45-885b-11c4e3d2b102"
    assert trading_result.volume == FakeTradingResultConfig.VOLUME
    assert trading_result.exchange_product_id == FakeTradingResultConfig.EXCHANGE_PRODUCT_ID

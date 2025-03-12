import pytest

from app.domain.entities.trading_result import TradingResultEntity
from app.infrastructure.repositories.trading_result.base import TradingResultRepository
from app.infrastructure.services.trading_result import TradingResultService
from app.infrastructure.uow.trading_result.base import TradingResultUnitOfWork
from tests.unit_test.test_infrastructure.utils import create_fake_trading_repository_instance, \
    FakeTradingResultUnitOfWork, FakeTradingResultConfig


@pytest.mark.asyncio
async def test_users_service_get_user_by_id_success() -> None:
    tradings_repository: TradingResultRepository = await create_fake_trading_repository_instance(
        with_trading_result=True
    )

    users_unit_of_work: TradingResultUnitOfWork = FakeTradingResultUnitOfWork(
        products_market=tradings_repository,
    )

    trading_service: TradingResultService = TradingResultService(uow=users_unit_of_work)

    assert len(await tradings_repository.list()) == 1

    trading_result: TradingResultEntity = (await trading_service.get_by_exchange_product_id(
        exchange_product_id=FakeTradingResultConfig.EXCHANGE_PRODUCT_ID,
        page_number=1,
        page_size=1
    ))[0]

    assert trading_result.volume == FakeTradingResultConfig.VOLUME
    assert trading_result.oid == FakeTradingResultConfig.OID

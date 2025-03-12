from dataclasses import dataclass, asdict
from datetime import date
from typing import Dict, Any

from app.domain.entities.trading_result import TradingResultEntity
from app.domain.values.trading_result import Volume, Total, Count
from app.infrastructure.repositories.trading_result.base import TradingResultRepository
from app.infrastructure.uow.trading_result.base import TradingResultUnitOfWork
from tests.unit_test.test_infrastructure.services.fake_repositories import FakeTradingResultRepository


@dataclass
class BaseTestConfig:

    def to_dict(self, to_lower: bool = False) -> Dict[str, Any]:
        base_dict: Dict[str, Any] = asdict(self)
        if to_lower:
            return {k.lower(): v for k, v in base_dict.items()}

        return base_dict


@dataclass
class FakeTradingResultConfig(BaseTestConfig):
    OID: str = "0866a2c2-a9fe-4f45-885b-11c4e3d2b102"
    EXCHANGE_PRODUCT_ID: str = 'A100ANK060F'
    EXCHANGE_PRODUCT_NAME: str = "Бензин (АИ-100-К5), Ангарск-группа станций (ст. отправления)"
    DELIVERY_BASIS_NAME: str = "Ангарск-группа станций"
    VOLUME: Volume = Volume(60)
    TOTAL: Total = Total(4000000)
    COUNT: Count = Count(1)
    DATE: date = date.today()


async def create_fake_trading_repository_instance(with_trading_result: bool = False) -> TradingResultRepository:
    tradings_repository: TradingResultRepository

    if with_trading_result:
        tradings_data: FakeTradingResultConfig = FakeTradingResultConfig()

        test_data = tradings_data.to_dict(to_lower=True)
        test_data["volume"] = Volume(test_data["volume"]["value"])

        entities: TradingResultEntity = TradingResultEntity(**test_data)
        users_repository = FakeTradingResultRepository(trading_results={FakeTradingResultConfig.OID: entities})
    else:
        users_repository = FakeTradingResultRepository()

    return users_repository


class FakeTradingResultUnitOfWork(TradingResultUnitOfWork):

    def __init__(
            self,
            products_market: TradingResultRepository,
    ) -> None:

        super().__init__()
        self.products_market = products_market
        self.committed: bool = False

    async def commit(self) -> None:
        self.committed = True

    async def rollback(self) -> None:
        pass

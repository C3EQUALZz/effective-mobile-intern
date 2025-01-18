from typing import Self

from infrastructure.repositories.trading_result.alchemy import SQLAlchemyTradingResultRepository
from infrastructure.repositories.trading_result.base import TradingResultRepository
from infrastructure.uow.base import SQLAlchemyAbstractUnitOfWork
from infrastructure.uow.trading_result.base import TradingResultUnitOfWork


class SQLAlchemyTradingResultUnitOfWork(SQLAlchemyAbstractUnitOfWork, TradingResultUnitOfWork):
    async def __aenter__(self) -> Self:
        uow = await super().__aenter__()
        self.products_market: TradingResultRepository = SQLAlchemyTradingResultRepository(session=self._session)
        return uow

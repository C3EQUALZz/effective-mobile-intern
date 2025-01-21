from typing import Self

from app.infrastructure.repositories.trading_result.alchemy import SQLAlchemyTradingResultRepository
from app.infrastructure.repositories.trading_result.base import TradingResultRepository
from app.infrastructure.uow.base import SQLAlchemyAbstractUnitOfWork
from app.infrastructure.uow.trading_result.base import TradingResultUnitOfWork


class SQLAlchemyTradingResultUnitOfWork(SQLAlchemyAbstractUnitOfWork, TradingResultUnitOfWork):
    async def __aenter__(self) -> Self:
        uow = await super().__aenter__()
        self.products_market: TradingResultRepository = SQLAlchemyTradingResultRepository(session=self._session)
        return uow

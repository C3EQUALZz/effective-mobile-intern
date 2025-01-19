from typing import List, Optional

from sqlalchemy import Result, insert
from typing_extensions import override

from domain.entities.trading_result import TradingResultEntity
from infrastructure.repositories.base import SQLAlchemyAbstractRepository
from infrastructure.repositories.trading_result.base import TradingResultRepository


class SQLAlchemyTradingResultRepository(SQLAlchemyAbstractRepository, TradingResultRepository):

    @override
    async def get_by_exchange_product_name(self, name: str) -> List[TradingResultEntity]:
        raise NotImplementedError

    @override
    async def get_by_delivery_basis_name(self, name: str) -> List[TradingResultEntity]:
        raise NotImplementedError

    @override
    async def add(self, model: TradingResultEntity) -> TradingResultEntity:
        result: Result = await self._session.execute(
            insert(TradingResultEntity).values(**await model.to_dict()).returning(TradingResultEntity)
        )

        return result.scalar_one()

    @override
    async def get(self, oid: str) -> Optional[TradingResultEntity]:
        raise NotImplementedError

    @override
    async def update(self, oid: str, model: TradingResultEntity) -> TradingResultEntity:
        raise NotImplementedError

    @override
    async def list(self, start: int = 0, limit: int = 10) -> List[TradingResultEntity]:
        raise NotImplementedError

    @override
    async def delete(self, oid: str) -> Optional[TradingResultEntity]:
        raise NotImplementedError

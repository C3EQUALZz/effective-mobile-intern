from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    List,
    Optional,
)

from app.domain.entities.trading_result import TradingResultEntity
from app.infrastructure.repositories.base import AbstractRepository


class TradingResultRepository(AbstractRepository[TradingResultEntity], ABC):
    """
    An interface for work with TradingResult, that is used by TradingResult unit of work.
    The main goal is that implementations of this interface can be easily replaced in TradingResult unit of work
    using dependency injection without disrupting its functionality.
    """

    @abstractmethod
    async def get_by_exchange_product_id(self, exchange_product_id: str) -> Optional[TradingResultEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_exchange_product_name(self, name: str) -> List[TradingResultEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_delivery_basis_name(self, name: str) -> List[TradingResultEntity]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, model: TradingResultEntity) -> TradingResultEntity:
        raise NotImplementedError

    @abstractmethod
    async def get(self, oid: str) -> Optional[TradingResultEntity]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, oid: str, model: TradingResultEntity) -> TradingResultEntity:
        raise NotImplementedError

    @abstractmethod
    async def list(self, start: int = 0, limit: int = 10) -> List[TradingResultEntity]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, oid: str) -> Optional[TradingResultEntity]:
        raise NotImplementedError

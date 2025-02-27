import builtins
from abc import (
    ABC,
    abstractmethod,
)
from datetime import date
from typing import Optional

from app.domain.entities.trading_result import TradingResultEntity
from app.infrastructure.repositories.base import AbstractRepository


class TradingResultRepository(AbstractRepository[TradingResultEntity], ABC):
    """
    An interface for work with TradingResult, that is used by TradingResult unit of work.
    The main goal is that implementations of this interface can be easily replaced in TradingResult unit of work
    using dependency injection without disrupting its functionality.
    """

    @abstractmethod
    async def get_by_exchange_product_id(
            self,
            exchange_product_id: str,
            start: int = 0,
            limit: int = 10
    ) -> list[TradingResultEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_exchange_product_name(
            self,
            name: str,
            start: int = 0,
            limit: int = 10
    ) -> list[TradingResultEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_delivery_basis_name(
            self,
            name: str,
            start: int = 0,
            limit: int = 10
    ) -> list[TradingResultEntity]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, model: TradingResultEntity) -> TradingResultEntity:
        raise NotImplementedError

    @abstractmethod
    async def get(self, oid: str) -> TradingResultEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, oid: str, model: TradingResultEntity) -> TradingResultEntity:
        raise NotImplementedError

    @abstractmethod
    async def list(self, start: int = 0, limit: int = 10) -> list[TradingResultEntity]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_date(
            self,
            start_date: date,
            end_date: date,
            start: int = 0,
            limit: int = 10
    ) -> builtins.list[TradingResultEntity]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, oid: str) -> TradingResultEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def list_filtered(
            self,
            oil_id: Optional[str],
            delivery_type_id: Optional[str],
            delivery_basis_id: Optional[str],
            start: int = 0,
            limit: int = 10
    ) -> builtins.list[TradingResultEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_unique_trading_dates(
            self,
            start_date: date,
            end_date: date,
            start: int = 0,
            limit: int = 10
    ) -> builtins.list[date]:
        raise NotImplementedError

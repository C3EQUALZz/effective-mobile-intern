import builtins
from datetime import date
from typing import Optional

from app.domain.entities.trading_result import TradingResultEntity
from app.infrastructure.repositories.trading_result.base import TradingResultRepository


class FakeTradingResultRepository(TradingResultRepository):
    def __init__(self, trading_results: Optional[dict[str, TradingResultEntity]] = None) -> None:
        self.trading_results: dict[str, TradingResultEntity] = trading_results if trading_results else {}

    async def get_by_exchange_product_id(
            self,
            exchange_product_id: str,
            start: int = 0,
            limit: int = 10
    ) -> list[TradingResultEntity]:
        return list(
            filter(
                lambda x: x.exchange_product_id == exchange_product_id,
                self.trading_results.values()
            )
        )[start:start + limit]

    async def get_by_exchange_product_name(
            self,
            name: str,
            start: int = 0,
            limit: int = 10
    ) -> list[TradingResultEntity]:
        return list(
            filter(
                lambda x: x.exchange_product_name == name,
                self.trading_results.values()
            )
        )[start:start + limit]

    async def get_by_delivery_basis_name(
            self,
            name: str,
            start: int = 0,
            limit: int = 10
    ) -> list[TradingResultEntity]:
        return list(
            filter(
                lambda x: x.delivery_basis_name == name,
                self.trading_results.values()
            )
        )[start:start + limit]

    async def add(self, model: TradingResultEntity) -> TradingResultEntity:
        trading_result: TradingResultEntity = TradingResultEntity(**await model.to_dict())
        self.trading_results[trading_result.oid] = trading_result
        return trading_result

    async def get(self, oid: str) -> TradingResultEntity | None:
        return self.trading_results.get(oid)

    async def update(self, oid: str, model: TradingResultEntity) -> TradingResultEntity:
        trading_result: TradingResultEntity = TradingResultEntity(**await model.to_dict())
        if oid in self.trading_results:
            self.trading_results[oid] = trading_result

        return trading_result

    async def list(self, start: int = 0, limit: int = 10) -> list[TradingResultEntity]:
        return list(self.trading_results.values())

    async def list_by_date(
            self,
            start_date: date,
            end_date: date,
            start: int = 0,
            limit: int = 10
    ) -> builtins.list[TradingResultEntity]:
        return list(
            filter(
                lambda x: start_date <= x.date <= end_date,
                self.trading_results.values()
            )
        )[start:start + limit]

    async def delete(self, oid: str) -> TradingResultEntity | None:
        if oid in self.trading_results:
            del self.trading_results[oid]

    async def list_filtered(
            self,
            oil_id: Optional[str],
            delivery_type_id: Optional[str],
            delivery_basis_id: Optional[str],
            start: int = 0,
            limit: int = 10
    ) -> builtins.list[TradingResultEntity]:

        all_values = self.trading_results.values()

        if oil_id is not None:
            all_values = filter(lambda x: x.oil_id == oil_id, all_values)
        if delivery_type_id is not None:
            all_values = filter(lambda x: x.delivery_type_id == delivery_type_id, all_values)
        if delivery_basis_id is not None:
            all_values = filter(lambda x: x.delivery_basis_id == delivery_basis_id, all_values)

        return list(all_values)[start:start + limit]

    async def get_unique_trading_dates(
            self,
            start_date: date,
            end_date: date,
            start: int = 0,
            limit: int = 10
    ) -> builtins.list[date]:
        all_unique_values = set((filter(lambda x: start_date <= x.date <= end_date, self.trading_results.values())))
        return list(all_unique_values)[start:start + limit]

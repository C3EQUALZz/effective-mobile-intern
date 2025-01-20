from datetime import date
from typing import Self

from domain.entities.trading_result import TradingResultEntity
from pydantic import BaseModel


class ParseAllBulletinsSpimexRequest(BaseModel):
    start_date: date
    end_date: date


class TradingResultsSpimexRequest(BaseModel):
    exchange_product_id: str
    exchange_product_name: str
    delivery_basis_name: str
    volume: int
    total: int
    count: int
    date: date

    @classmethod
    def from_entity(cls, entity: TradingResultEntity) -> Self:
        return cls(
            exchange_product_id=entity.exchange_product_id,
            exchange_product_name=entity.exchange_product_name,
            delivery_basis_name=entity.delivery_basis_name,
            volume=entity.volume.as_generic_type(),
            total=entity.total.as_generic_type(),
            count=entity.count.as_generic_type(),
            date=entity.date,
        )

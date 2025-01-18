from dataclasses import dataclass, field
from datetime import datetime, UTC

from domain.entities.base import BaseEntity
from domain.values.trading_result import Count, Total, Volume


@dataclass(slots=True)
class TradingResultEntity(BaseEntity):
    exchange_product_id: str
    exchange_product_name: str
    delivery_basis_name: str
    volume: Volume
    total: Total
    count: Count
    date: datetime
    created_on: datetime = field(default_factory=lambda: datetime.now(UTC), kw_only=True)
    updated_on: datetime = field(default_factory=lambda: datetime.now(UTC), kw_only=True)

    @property
    def oil_id(self) -> str:
        return self.exchange_product_id[:4]

    @property
    def delivery_basis_id(self) -> str:
        return self.exchange_product_id[4:7]

    @property
    def delivery_type_id(self) -> str:
        return self.exchange_product_id[-1]

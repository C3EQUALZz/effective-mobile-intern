from dataclasses import (
    dataclass,
    field,
)
from datetime import (
    UTC,
    date,
    datetime,
)

from app.domain.entities.base import BaseEntity
from app.domain.values.trading_result import (
    Count,
    Total,
    Volume,
)


@dataclass(slots=True)
class TradingResultEntity(BaseEntity):
    exchange_product_id: str
    exchange_product_name: str
    delivery_basis_name: str
    volume: Volume
    total: Total
    count: Count
    date: date
    created_on: date = field(default_factory=lambda: datetime.now(UTC).date(), kw_only=True)
    updated_on: date = field(default_factory=lambda: datetime.now(UTC).date(), kw_only=True)

    @property
    def oil_id(self) -> str:
        return self.exchange_product_id[:4]

    @property
    def delivery_basis_id(self) -> str:
        return self.exchange_product_id[4:7]

    @property
    def delivery_type_id(self) -> str:
        return self.exchange_product_id[-1]

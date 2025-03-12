from sqlalchemy import (
    Column,
    DateTime,
    String,
    Table,
    func
)

from app.infrastructure.adapters.alchemy.metadata import (
    mapper_registry,
    metadata,
)
from app.infrastructure.adapters.alchemy.type_decorators import VolumeDecorator, TotalDecorator, CountDecorator

spimex_trading_results_table = Table(
    "spimex_trading_results",
    metadata,
    Column("oid", String, primary_key=True),
    Column("exchange_product_id", String),
    Column("exchange_product_name", String),
    Column("oil_id", String, server_default=func.substr("exchange_product_id", 1, 4)),
    Column("delivery_basis_id", String, server_default=func.substr("exchange_product_id", 5, 3)),
    Column("delivery_basis_name", String),
    Column("delivery_type_id", String, server_default=func.substr("exchange_product_id", 8, 1)),
    Column("volume", VolumeDecorator),
    Column("total", TotalDecorator),
    Column("count", CountDecorator),
    Column("date", DateTime),
    Column("created_on", DateTime),
    Column("updated_on", DateTime),
)


def start_mappers() -> None:
    """
    Map all domain models to ORM models, for purpose of using domain models directly during work with the database,
    according to DDD.
    """
    from app.domain.entities.trading_result import TradingResultEntity

    mapper_registry.map_imperatively(TradingResultEntity, spimex_trading_results_table)

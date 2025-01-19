from sqlalchemy import Table, Column, Integer, String, DateTime, Uuid

from app.infrastructure.adapters.alchemy.metadata import mapper_registry
from app.infrastructure.adapters.alchemy.metadata import metadata

spimex_trading_results_table = Table(
    "spimex_trading_results",
    metadata,
    Column("oid", Uuid, primary_key=True),
    Column("exchange_product_id", String),
    Column("exchange_product_name", String),
    Column("oil_id", String),
    Column("delivery_basis_id", String),
    Column("delivery_basis_name", String),
    Column("delivery_type_id", String),
    Column("volume", Integer),
    Column("total", Integer),
    Column("count", Integer),
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

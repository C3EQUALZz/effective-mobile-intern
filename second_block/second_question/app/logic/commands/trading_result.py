from dataclasses import dataclass
from datetime import date

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class GetByIdCommand(AbstractCommand):
    oid: str


@dataclass(frozen=True)
class GetByExchangeProductId(AbstractCommand):
    exchange_product_id: str
    page_number: int
    page_size: int


@dataclass(frozen=True)
class GetByExchangeProductName(AbstractCommand):
    exchange_product_name: str
    page: int
    size: int


@dataclass(frozen=True)
class GetByDeliveryBasisName(AbstractCommand):
    delivery_basis_name: str
    page: int
    size: int


@dataclass(frozen=True)
class ParseAllBulletinsFromSphinx(AbstractCommand):
    start_date: date
    end_date: date


@dataclass(frozen=True)
class GetListOfTradesForSpecifiedPeriod(AbstractCommand):
    start_date: date
    end_date: date
    page_number: int
    page_size: int


@dataclass(frozen=True)
class GetLastTradingDates(AbstractCommand):
    count_of_days: int
    page_number: int
    page_size: int


@dataclass(frozen=True)
class GetTradingResults(AbstractCommand):
    oil_id: str
    delivery_type_id: str
    delivery_basis_id: str
    page_number: int
    page_size: int

from abc import ABC

from app.infrastructure.repositories.trading_result.base import TradingResultRepository
from app.infrastructure.uow.base import AbstractUnitOfWork


class TradingResultUnitOfWork(AbstractUnitOfWork, ABC):
    """
    An interface for work with books, that is used by service layer of books module.
    The main goal is that implementations of this interface can be easily replaced in the service layer
    using dependency injection without disrupting its functionality.
    """

    products_market: TradingResultRepository

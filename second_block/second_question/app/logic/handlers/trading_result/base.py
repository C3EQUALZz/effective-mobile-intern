from abc import ABC

from app.infrastructure.uow.trading_result.base import TradingResultUnitOfWork
from app.logic.handlers.base import (
    CT,
    ET,
    AbstractCommandHandler,
    AbstractEventHandler,
)


class TradingResultEventHandler(AbstractEventHandler[ET], ABC):
    """
    Abstract event handler class, from which every users event handler should be inherited from.
    """

    def __init__(self, uow: TradingResultUnitOfWork) -> None:
        self._uow: TradingResultUnitOfWork = uow


class TradingResultCommandHandler(AbstractCommandHandler[CT], ABC):
    """
    Abstract command handler class, from which every users command handler should be inherited from.
    """

    def __init__(self, uow: TradingResultUnitOfWork) -> None:
        self._uow: TradingResultUnitOfWork = uow

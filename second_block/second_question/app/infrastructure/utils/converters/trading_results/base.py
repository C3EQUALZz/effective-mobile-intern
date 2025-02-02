from abc import ABC, abstractmethod
from datetime import date
from io import BytesIO
from typing import AsyncGenerator

from domain.entities.trading_result import TradingResultEntity


class AbstractDocumentConverter(ABC):
    @abstractmethod
    async def convert(self, file_content: BytesIO, date_of_creation: date) -> AsyncGenerator[TradingResultEntity, None]:
        raise NotImplementedError

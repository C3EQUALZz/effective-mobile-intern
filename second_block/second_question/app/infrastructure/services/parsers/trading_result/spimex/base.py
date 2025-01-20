import io
from abc import (
    ABC,
    abstractmethod,
)
from collections.abc import AsyncGenerator
from datetime import date

from app.infrastructure.services.parsers.base import Parser


class AbstractSpimexParser(Parser, ABC):
    @abstractmethod
    async def parse(self, *args, **kwargs) -> AsyncGenerator[tuple[date, io.BytesIO], None]: ...

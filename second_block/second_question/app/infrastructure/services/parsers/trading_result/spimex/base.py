import io
from abc import ABC, abstractmethod
from datetime import date
from typing import AsyncGenerator, Tuple

from app.infrastructure.services.parsers.base import Parser


class AbstractSpimexParser(Parser, ABC):
    @abstractmethod
    async def parse(self, *args, **kwargs) -> AsyncGenerator[Tuple[date, io.BytesIO], None]:
        ...

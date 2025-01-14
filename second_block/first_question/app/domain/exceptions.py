from abc import ABC
from dataclasses import dataclass

from app.exceptions import ApplicationException


@dataclass(eq=False)
class DomainException(ApplicationException, ABC):
    @property
    def message(self) -> str:
        return "Exception on domain layer"


@dataclass(eq=False)
class CastException(DomainException):
    text: str

    @property
    def message(self) -> str:
        return f"Failed to cast field {self.text}"

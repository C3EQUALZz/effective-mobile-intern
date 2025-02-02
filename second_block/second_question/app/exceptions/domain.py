from exceptions.base import ApplicationException
from dataclasses import dataclass
from abc import ABC
from http import HTTPStatus


@dataclass(eq=False)
class DomainException(ApplicationException, ABC):
    @property
    def message(self) -> str:
        return "Exception on domain layer"

    @property
    def status(self) -> int:
        return HTTPStatus.UNPROCESSABLE_ENTITY.value


@dataclass(eq=False)
class VolumeException(DomainException):
    @property
    def message(self) -> str:
        return "Volume can't be negative"


@dataclass(eq=False)
class CountException(DomainException):
    @property
    def message(self) -> str:
        return "Count can't be negative"


@dataclass(eq=False)
class TotalException(DomainException):
    @property
    def message(self) -> str:
        return "Total can't be negative"

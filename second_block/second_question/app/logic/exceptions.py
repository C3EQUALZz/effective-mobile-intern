from abc import (
    ABC,
)
from dataclasses import dataclass
from http import HTTPStatus

from app.exceptions import ApplicationException


@dataclass(eq=False)
class LogicException(ApplicationException, ABC):
    @property
    def message(self) -> str:
        return "An logic error has occurred"


@dataclass(eq=False)
class MessageBusMessageException(LogicException):
    @property
    def message(self) -> str:
        return "Message bus message should be eiter of Event type, or Command type"

    @property
    def status(self) -> int:
        return HTTPStatus.BAD_REQUEST.value

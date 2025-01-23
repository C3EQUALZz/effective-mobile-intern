from abc import ABC
from dataclasses import dataclass
from http import HTTPStatus

from dogs.exceptions.base import ApplicationException


@dataclass(eq=False)
class DomainException(ApplicationException, ABC):
    @property
    def message(self) -> str:
        return "Exception on domain layer"

    @property
    def status(self) -> int:
        return HTTPStatus.UNPROCESSABLE_ENTITY.value


@dataclass(eq=False)
class CastException(DomainException):
    text: str

    @property
    def message(self) -> str:
        return f"Failed to cast field {self.text}"


@dataclass(eq=False)
class BadNameException(DomainException):
    value: str

    @property
    def message(self) -> str:
        return f"Name {self.value} is invalid, don't use digits, only letters"


@dataclass(eq=False)
class BadDogAgeException(DomainException):
    value: str

    @property
    def message(self) -> str:
        return f"Dog age {self.value} is invalid"


@dataclass(eq=False)
class BadDogGenException(DomainException):
    value: str

    @property
    def message(self) -> str:
        return f"Dog gen {self.value} is invalid. It can be only: female, male."


@dataclass(eq=False)
class BadDogColorException(DomainException):
    value: str

    @property
    def message(self) -> str:
        return f"Dog color {self.value} is invalid"


@dataclass(eq=False)
class BadDogFavouriteFoodException(DomainException):
    value: str

    @property
    def message(self) -> str:
        return f"Dog food {self.value} is invalid"


@dataclass(eq=False)
class BadDogFavouriteToyException(DomainException):
    value: str

    @property
    def message(self) -> str:
        return f"Dog toy {self.value} is invalid"


@dataclass(eq=False)
class SizeException(DomainException):
    value: str

    @property
    def message(self) -> str:
        return f"Size {self.value} is invalid. It can be only: 'Tiny', 'Small', 'Medium', 'Large'"

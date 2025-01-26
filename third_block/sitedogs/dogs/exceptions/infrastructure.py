from abc import ABC
from dataclasses import dataclass
from http import HTTPStatus

from dogs.exceptions.base import ApplicationException


@dataclass(eq=False)
class InfrastructureException(ApplicationException, ABC):
    @property
    def message(self) -> str:
        return "Infrastructure exception has occurred"

    @property
    def status(self) -> int:
        return HTTPStatus.INTERNAL_SERVER_ERROR.value


@dataclass(eq=False)
class DogNotFoundException(InfrastructureException):
    value: str

    @property
    def message(self) -> str:
        return f"Dog with param {self.value} not found"

    @property
    def status(self) -> int:
        return HTTPStatus.NOT_FOUND.value


@dataclass(eq=False)
class BreedNotFoundException(InfrastructureException):
    value: str

    @property
    def message(self) -> str:
        return f"Breed with param {self.value} not found"

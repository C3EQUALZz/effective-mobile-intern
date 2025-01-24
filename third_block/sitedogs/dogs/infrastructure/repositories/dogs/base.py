from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    List,
    Optional, )

from typing import Literal

from dogs.domain.entities.dogs import DogEntity
from dogs.infrastructure.repositories.base import AbstractRepository


class DogsRepository(AbstractRepository[DogEntity], ABC):
    """
    An interface for work with users, that is used by users unit of work.
    The main goal is that implementations of this interface can be easily replaced in users unit of work
    using dependency injection without disrupting its functionality.
    """

    @abstractmethod
    def get_by_name(self, name: str) -> List[DogEntity]:
        raise NotImplementedError

    @abstractmethod
    def get_by_age(self, age: int) -> List[DogEntity]:
        raise NotImplementedError

    @abstractmethod
    def get_by_gender(self, gender: Literal["Male", "Female"]) -> List[DogEntity]:
        raise NotImplementedError

    @abstractmethod
    def add(self, model: DogEntity) -> DogEntity:
        raise NotImplementedError

    @abstractmethod
    def get(self, oid: str) -> Optional[DogEntity]:
        raise NotImplementedError

    @abstractmethod
    def update(self, oid: str, model: DogEntity) -> DogEntity:
        raise NotImplementedError

    @abstractmethod
    def list(self, start: int = 0, limit: int = 10) -> List[DogEntity]:
        raise NotImplementedError

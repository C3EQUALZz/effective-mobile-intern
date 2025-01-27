from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    List,
    Literal,
    Optional,
)

from dogs.domain.entities.dogs import DogEntity
from dogs.infrastructure.adapters.django_orm.dogs import DogsAdapter
from dogs.infrastructure.adapters.dto.dogs import DogsWithAverageAgeForEachBreed
from dogs.infrastructure.repositories.base import AbstractRepository


class DogsRepository(AbstractRepository[DogEntity, DogsAdapter], ABC):
    """
    An interface for work with users, that is used by users unit of work.
    The main goal is that implementations of this interface can be easily replaced in users unit of work
    using dependency injection without disrupting its functionality.
    """

    @abstractmethod
    def get_by_name_age_gender(self, name: str, age: int, gender: Literal["Male", "Female"]) -> List[DogEntity]:
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

    @abstractmethod
    def list_dogs_with_average_age_for_each_breed(
        self, start: int = 0, limit: int = 10
    ) -> List[DogsWithAverageAgeForEachBreed]:
        raise NotImplementedError

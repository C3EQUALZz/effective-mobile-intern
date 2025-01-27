from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    List,
    Optional,
)

from dogs.domain.entities.breed import BreedEntity
from dogs.infrastructure.adapters.django_orm.breeds import BreedsAdapter
from dogs.infrastructure.adapters.dto.breeds import BreedWithCountOfDogs
from dogs.infrastructure.repositories.base import AbstractRepository


class BreedsRepository(AbstractRepository[BreedEntity, BreedsAdapter], ABC):
    """
    An interface for work with breeds.
    The main goal is that implementations of this interface can be easily replaced in users unit of work or in service
    using dependency injection without disrupting its functionality.
    """

    def __init__(self, adapter: BreedsAdapter) -> None:
        super().__init__(adapter)

    @abstractmethod
    def add(self, model: BreedEntity) -> BreedEntity:
        raise NotImplementedError

    @abstractmethod
    def get(self, oid: str) -> Optional[BreedEntity]:
        raise NotImplementedError

    @abstractmethod
    def update(self, oid: str, model: BreedEntity) -> BreedEntity:
        raise NotImplementedError

    @abstractmethod
    def list(self, start: int = 0, limit: int = 10) -> List[BreedEntity]:
        raise NotImplementedError

    @abstractmethod
    def list_with_count_for_each_breed(self, start: int = 0, limit: int = 10) -> List[BreedWithCountOfDogs]:
        raise NotImplementedError
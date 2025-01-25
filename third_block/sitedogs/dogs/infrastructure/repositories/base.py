from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Generic,
    List,
    Optional,
    TypeVar,
)

from dogs.domain.entities.base import BaseEntity
from dogs.infrastructure.adapters.django_orm.base import BaseAdapter

BaseEntityType = TypeVar("BaseEntityType", bound=BaseEntity)
BaseAdapterType = TypeVar("BaseAdapterType", bound=BaseAdapter)


class AbstractRepository(ABC, Generic[BaseEntityType, BaseAdapterType]):
    """
    Interface for any repository, which would be used for work with domain model, according DDD.

    Main purpose is to encapsulate internal logic that is associated with the use of one or another data
    storage scheme, for example, ORM.
    """

    def __init__(self, adapter: BaseAdapterType) -> None:
        self._adapter = adapter

    @abstractmethod
    def add(self, model: BaseEntityType) -> BaseEntityType:
        raise NotImplementedError

    @abstractmethod
    def get(self, oid: str) -> Optional[BaseEntityType]:
        raise NotImplementedError

    @abstractmethod
    def update(self, oid: str, model: BaseEntityType) -> BaseEntityType:
        raise NotImplementedError

    @abstractmethod
    def delete(self, oid: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(self, start: int = 0, limit: int = 10) -> List[BaseEntityType]:
        raise NotImplementedError

from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Generic,
    TypeVar,
)

from django.db.models.base import Model

from dogs.domain.entities.base import BaseEntity


ModelType = TypeVar('ModelType', bound=Model)
EntityType = TypeVar('EntityType', bound=BaseEntity)


class BaseAdapter(ABC, Generic[ModelType, EntityType]):
    @abstractmethod
    def to_entity(self, model: ModelType) -> EntityType:
        raise NotImplementedError

    @abstractmethod
    def to_model(self, entity: EntityType) -> ModelType:
        raise NotImplementedError

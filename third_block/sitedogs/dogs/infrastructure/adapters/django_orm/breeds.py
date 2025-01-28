from typing import override

from core.infrastructure.adapters.django_orm.base import BaseAdapter

from dogs.domain.entities.breed import BreedEntity
from dogs.domain.values.breed import (
    ExerciseNeeds,
    Friendliness,
    SheddingAmount,
    Size,
    TrainAbility,
)
from dogs.domain.values.shared import Name
from dogs.infrastructure.adapters.django_orm.orm import Breed


class BreedsAdapter(BaseAdapter[Breed, BreedEntity]):
    @override
    def to_entity(self, model: Breed) -> BreedEntity:
        breed: BreedEntity = BreedEntity(
            oid=str(model.oid),
            name=Name(model.name),
            size=Size(model.size),
            friendliness=Friendliness(model.friendliness),
            train_ability=TrainAbility(model.train_ability),
            shedding_amount=SheddingAmount(model.shedding_amount),
            exercise_needs=ExerciseNeeds(model.exercise_needs),
        )

        return breed

    @override
    def to_model(self, entity: BreedEntity) -> Breed:
        breed: Breed = Breed(
            oid=entity.oid,
            name=entity.name.as_generic_type(),
            size=entity.size.as_generic_type(),
            friendliness=entity.friendliness.as_generic_type(),
            train_ability=entity.train_ability.as_generic_type(),
            shedding_amount=entity.shedding_amount.as_generic_type(),
            exercise_needs=entity.exercise_needs.as_generic_type(),
        )

        return breed

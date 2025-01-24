from typing import override

from dogs.domain.entities.breed import Breed
from dogs.domain.entities.dogs import DogEntity
from dogs.domain.values.dog import Age, Gender, FavouriteFood, FavouriteToy, Color
from dogs.domain.values.shared import Name
from dogs.infrastructure.adapters.base import BaseAdapter
from dogs.infrastructure.adapters.django_orm.orm import Dog


class DogsAdapter(BaseAdapter[Dog, DogEntity]):

    @override
    def to_entity(self, model: Dog) -> DogEntity:

        breed: Breed = Breed(
            name=model.breed.name,
            size=model.breed.size,
            friendliness=model.breed.friendliness,
            train_ability=model.breed.train_ability,
            shedding_amount=model.breed.shedding_amount,
            exercise_needs=model.breed.exercise_needs,
        )

        return DogEntity(
            oid=model.oid,
            name=Name(model.name),
            age=Age(model.age),
            breed=breed,
            gender=Gender(model.gender),
            color=Color(model.color),
            favorite_food=FavouriteFood(model.favorite_food),
            favorite_toy=FavouriteToy(model.favorite_toy),
        )

    @override
    def to_model(self, entity: DogEntity) -> Dog:
        ...

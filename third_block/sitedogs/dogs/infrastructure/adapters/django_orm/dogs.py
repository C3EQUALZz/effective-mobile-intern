from typing import override

from dogs.domain.entities.breed import BreedEntity
from dogs.domain.entities.dogs import DogEntity
from dogs.domain.values.breed import Size, Friendliness, TrainAbility, SheddingAmount, ExerciseNeeds
from dogs.domain.values.dog import Age, Gender, FavouriteFood, FavouriteToy, Color
from dogs.domain.values.shared import Name
from dogs.infrastructure.adapters.django_orm.base import BaseAdapter
from dogs.infrastructure.adapters.django_orm.orm import Dog, Breed


class DogsAdapter(BaseAdapter[Dog, DogEntity]):
    @override
    def to_entity(self, model: Dog) -> DogEntity:
        breed: BreedEntity = BreedEntity(
            name=Name(model.breed.name),
            size=Size(model.breed.size),
            friendliness=Friendliness(model.breed.friendliness),
            train_ability=TrainAbility(model.breed.train_ability),
            shedding_amount=SheddingAmount(model.breed.shedding_amount),
            exercise_needs=ExerciseNeeds(model.breed.exercise_needs),
        )

        return DogEntity(
            oid=str(model.oid),
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
        breed: Breed = Breed(
            oid=entity.breed.oid,
            name=entity.breed.name.as_generic_type(),
            size=entity.breed.size.as_generic_type(),
            friendliness=entity.breed.friendliness.as_generic_type(),
            train_ability=entity.breed.train_ability.as_generic_type(),
            shedding_amount=entity.breed.shedding_amount.as_generic_type(),
            exercise_needs=entity.breed.exercise_needs.as_generic_type(),
        )

        dog: Dog = Dog(
            oid=entity.oid,
            name=entity.name.as_generic_type(),
            age=entity.age.as_generic_type(),
            breed=breed,
            gender=entity.gender.as_generic_type(),
            color=entity.color.as_generic_type(),
            favorite_food=entity.favorite_food.as_generic_type(),
            favorite_toy=entity.favorite_toy.as_generic_type(),
        )

        return dog

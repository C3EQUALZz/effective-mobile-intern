from typing import (
    Literal,
    Self,
)
from uuid import UUID

from ninja import Schema
from pydantic import (
    PositiveInt,
    constr,
)

from dogs.application.api.v1.breeds.schemas import CreateBreedSchemaResponse
from dogs.domain.entities.dogs import DogEntity
from dogs.infrastructure.adapters.dto.dogs import DogsWithAverageAgeForEachBreed


class BaseDogSchema(Schema):
    oid: UUID
    name: constr(min_length=1)
    age: PositiveInt
    breed: CreateBreedSchemaResponse
    color: constr(min_length=1)
    favourite_food: constr(min_length=1)
    favourite_toy: constr(min_length=1)

    @classmethod
    def from_entity(cls, entity: DogEntity) -> Self:
        return cls(
            oid=UUID(entity.oid),
            name=entity.name.as_generic_type(),
            age=entity.age.as_generic_type(),
            color=entity.color.as_generic_type(),
            breed=CreateBreedSchemaResponse.from_entity(entity.breed),
            favourite_food=entity.favorite_food.as_generic_type(),
            favourite_toy=entity.favorite_toy.as_generic_type(),
        )


class CreateDogSchemaRequest(Schema):
    name: constr(min_length=1)
    age: PositiveInt
    breed_oid: UUID
    gender: Literal["Male", "Female"]
    color: constr(min_length=1)
    favourite_food: constr(min_length=1)
    favourite_toy: constr(min_length=1)


class UpdateDogSchemaRequest(Schema):
    oid: UUID
    name: constr(min_length=1)
    age: PositiveInt
    breed_oid: UUID
    gender: Literal["Male", "Female"]
    color: constr(min_length=1)
    favourite_food: constr(min_length=1)
    favourite_toy: constr(min_length=1)


class CreateDogSchemaResponse(BaseDogSchema): ...


class GetDogByOidSchemaResponse(BaseDogSchema): ...


class UpdateDogSchemaResponse(BaseDogSchema): ...


class GetAllDogsWithAverageAgeForEachBreedSchemeResponse(Schema):
    average_age: float
    breed_name: str
    dogs: list[BaseDogSchema]

    @classmethod
    def from_entity(cls, entity: DogsWithAverageAgeForEachBreed) -> Self:
        return cls(
            average_age=entity.average_age,
            breed_name=entity.breed_name,
            dogs=[BaseDogSchema.from_entity(x) for x in entity.dogs],
        )

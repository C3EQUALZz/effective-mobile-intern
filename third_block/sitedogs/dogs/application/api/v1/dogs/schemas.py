from typing import Literal
from typing import Self
from uuid import UUID

from ninja import Schema
from pydantic import PositiveInt, constr

from dogs.application.api.v1.breeds.schemas import CreateBreedSchemaResponse
from dogs.domain.entities.dogs import DogEntity


class GetAllDogsSchemaResponse(Schema):
    ...


class GetDogsSchemaResponse(Schema):
    ...


class CreateDogSchemaRequest(Schema):
    name: constr(min_length=1)
    age: PositiveInt
    breed_oid: UUID
    gender: Literal["Male", "Female"]
    color: constr(min_length=1)
    favourite_food: constr(min_length=1)
    favourite_toy: constr(min_length=1)


class CreateDogSchemaResponse(Schema):
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

from typing import Literal

from ninja import Schema
from pydantic import PositiveInt, constr
from uuid import UUID

from dogs.domain.entities.breed import BreedEntity


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
    breed: BreedEntity
    color: constr(min_length=1)
    favourite_food: constr(min_length=1)
    favourite_toy: constr(min_length=1)

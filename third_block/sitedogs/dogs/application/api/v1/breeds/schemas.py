from typing import Literal, Self, cast
from uuid import UUID

from ninja import Schema
from pydantic import constr, conint

from dogs.domain.entities.breed import BreedEntity


class CreateBreedSchemaRequest(Schema):
    name: constr(min_length=1)
    size: Literal["Tiny", "Small", "Medium", "Large"]
    friendliness: conint(ge=1, le=5)
    train_ability: conint(ge=1, le=5)
    shedding_amount: conint(ge=1, le=5)
    exercise_needs: conint(ge=1, le=5)

class CreateBreedSchemaResponse(Schema):
    oid: UUID
    name: constr(min_length=1)
    size: Literal["Tiny", "Small", "Medium", "Large"]
    friendliness: conint(ge=1, le=5)
    train_ability: conint(ge=1, le=5)
    shedding_amount: conint(ge=1, le=5)
    exercise_needs: conint(ge=1, le=5)

    @classmethod
    def from_entity(cls, entity: BreedEntity) -> Self:
        return cls(
            oid=UUID(entity.oid),
            name=entity.name.as_generic_type(),
            size=cast(Literal["Tiny", "Small", "Medium", "Large"], entity.size.as_generic_type()),
            friendliness=entity.friendliness.as_generic_type(),
            train_ability=entity.train_ability.as_generic_type(),
            shedding_amount=entity.shedding_amount.as_generic_type(),
            exercise_needs=entity.exercise_needs.as_generic_type(),
        )

class UpdateBreedSchemaRequest(Schema):
    breed_oid: UUID
    name: constr(min_length=1)
    size: Literal["Tiny", "Small", "Medium", "Large"]
    friendliness: conint(ge=1, le=5)
    train_ability: conint(ge=1, le=5)
    shedding_amount: conint(ge=1, le=5)
    exercise_needs: conint(ge=1, le=5)

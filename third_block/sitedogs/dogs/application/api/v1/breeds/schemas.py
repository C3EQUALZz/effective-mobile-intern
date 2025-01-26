from typing import Literal
from uuid import UUID
from ninja import Schema
from pydantic import constr, conint


class CreateBreedSchemaRequest(Schema):
    name: constr(min_length=1)
    size: Literal["Tiny", "Small", "Medium", "Large"]
    friendliness: conint(ge=1, le=5)
    train_ability: conint(ge=1, le=5)
    shedding_amount: conint(ge=1, le=5)
    exercise_needs: conint(ge=1, le=5)


class UpdateBreedSchemaRequest(Schema):
    oid: UUID
    name: constr(min_length=1)
    size: Literal["Tiny", "Small", "Medium", "Large"]
    friendliness: conint(ge=1, le=5)
    train_ability: conint(ge=1, le=5)
    shedding_amount: conint(ge=1, le=5)
    exercise_needs: conint(ge=1, le=5)

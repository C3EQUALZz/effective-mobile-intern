from dataclasses import dataclass

from dogs.domain.entities.base import BaseEntity
from dogs.domain.values.breed import Size
from dogs.domain.values.shared import Name


@dataclass(eq=False)
class Breed(BaseEntity):
    name: Name
    size: Size
    friendliness: int
    train_ability: int
    shedding_amount: int
    exercise_needs: int

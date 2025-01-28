from dataclasses import dataclass

from core.domain.entities.base import BaseEntity

from dogs.domain.values.breed import (
    ExerciseNeeds,
    Friendliness,
    SheddingAmount,
    Size,
    TrainAbility,
)
from dogs.domain.values.shared import Name


@dataclass(eq=False)
class BreedEntity(BaseEntity):
    """
    Domain Entity that represents a breed of a dog.
    It has several attributes:
    - name: name of the breed. This field must be unique and non-empty.
    - size: size of the breed. This field cat take several values: "Tiny", "Small", "Medium", "Large".
    - friendliness: friendliness of the breed. This field cat take several values: 1 - 5.
    - train_ability: train_ability of the breed. This field cat take several values: 1 - 5.
    - shedding_amount: shedding_amount of the breed. This field cat take several values: 1 - 5.
    - exercise_needs: exercise_needs of the breed. This field cat take several values: 1 - 5.
    """
    name: Name
    size: Size
    friendliness: Friendliness
    train_ability: TrainAbility
    shedding_amount: SheddingAmount
    exercise_needs: ExerciseNeeds

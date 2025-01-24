from dataclasses import dataclass

from dogs.domain.entities.base import BaseEntity
from dogs.domain.values.breed import Size, Friendliness, TrainAbility, SheddingAmount, ExerciseNeeds
from dogs.domain.values.shared import Name


@dataclass(eq=False)
class Breed(BaseEntity):
    name: Name
    size: Size
    friendliness: Friendliness
    train_ability: TrainAbility
    shedding_amount: SheddingAmount
    exercise_needs: ExerciseNeeds

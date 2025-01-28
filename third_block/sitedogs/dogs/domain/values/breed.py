from dataclasses import dataclass
from typing import override

from core.domain.values.base import BaseValueObject

from dogs.exceptions.domain import (
    BadSizeException,
    BadValueBreedException,
)


@dataclass(frozen=True)
class Size(BaseValueObject):
    value: str

    @override
    def validate(self) -> None:
        if self.value not in ("Tiny", "Small", "Medium", "Large"):
            raise BadSizeException("Value must be one of 'Tiny', 'Small', 'Medium', 'Large'")

    @override
    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Friendliness(BaseValueObject):
    value: int

    @override
    def validate(self) -> None:
        if not 1 <= self.value <= 5:
            raise BadValueBreedException("Friendliness value must be between 1 and 5")

    @override
    def as_generic_type(self) -> int:
        return int(self.value)


@dataclass(frozen=True)
class TrainAbility(BaseValueObject):
    value: int

    @override
    def validate(self) -> None:
        if not 1 <= self.value <= 5:
            raise BadValueBreedException("Train ability value must be between 1 and 5")

    @override
    def as_generic_type(self) -> int:
        return int(self.value)


@dataclass(frozen=True)
class SheddingAmount(BaseValueObject):
    value: int

    @override
    def validate(self) -> None:
        if not 1 <= self.value <= 5:
            raise BadValueBreedException("Shedding amount value must be between 1 and 5")

    @override
    def as_generic_type(self) -> int:
        return int(self.value)


@dataclass(frozen=True)
class ExerciseNeeds(BaseValueObject):
    value: int

    @override
    def validate(self) -> None:
        if not 1 <= self.value <= 5:
            raise BadValueBreedException("Exercise needs value must be between 1 and 5")

    @override
    def as_generic_type(self) -> int:
        return int(self.value)

from dataclasses import dataclass
from typing import override

from dogs.domain.values.base import BaseValueObject
from dogs.exceptions.domain import SizeException


@dataclass(frozen=True)
class Size(BaseValueObject):
    value: int

    @override
    def validate(self) -> None:
        if self.value not in ("Tiny", "Small", "Medium", "Large"):
            raise SizeException("Value must be one of 'Tiny', 'Small', 'Medium', 'Large'")

    @override
    def as_generic_type(self) -> int:
        return int(self.value)


@dataclass(frozen=True)
class Friendliness(BaseValueObject):
    value: int

    @override
    def validate(self) -> None:
        if not 1 <= self.value <= 5:
            ...

    @override
    def as_generic_type(self) -> int:
        return int(self.value)

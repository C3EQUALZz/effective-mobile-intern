from typing import override

from domain.values.base import BaseValueObject
from dataclasses import dataclass


@dataclass(frozen=True)
class Count(BaseValueObject):
    value: int

    @override
    def validate(self) -> None:
        ...

    @override
    def as_generic_type(self) -> int:
        return int(self.value)


@dataclass(frozen=True)
class Volume(BaseValueObject):
    value: int

    @override
    def validate(self) -> None:
        ...

    @override
    def as_generic_type(self) -> int:
        return int(self.value)


@dataclass(frozen=True)
class Total(BaseValueObject):
    value: int

    @override
    def validate(self) -> None:
        ...

    @override
    def as_generic_type(self) -> int:
        return int(self.value)

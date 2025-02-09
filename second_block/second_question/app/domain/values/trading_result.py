from dataclasses import dataclass
from typing import override

from app.domain.values.base import BaseValueObject
from app.exceptions.domain import VolumeException, CountException, TotalException


@dataclass(frozen=True)
class Count(BaseValueObject):
    value: int

    @override
    def validate(self) -> None:
        if self.value < 0:
            raise CountException

    @override
    def as_generic_type(self) -> int:
        return int(self.value)


@dataclass(frozen=True)
class Volume(BaseValueObject):
    value: int

    @override
    def validate(self) -> None:
        if self.value < 0:
            raise VolumeException

    @override
    def as_generic_type(self) -> int:
        return int(self.value)


@dataclass(frozen=True)
class Total(BaseValueObject):
    value: int

    @override
    def validate(self) -> None:
        if self.value < 0:
            raise TotalException

    @override
    def as_generic_type(self) -> int:
        return int(self.value)

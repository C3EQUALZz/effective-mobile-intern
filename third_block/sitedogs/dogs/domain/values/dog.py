import re
from dataclasses import dataclass
from typing import (
    Literal,
    override,
)

from dogs.domain.values.base import BaseValueObject
from dogs.exceptions.domain import (
    BadDogAgeException,
    BadDogColorException,
    BadDogFavouriteFoodException,
    BadDogFavouriteToyException,
)


@dataclass(frozen=True)
class Age(BaseValueObject):
    value: int

    @override
    def validate(self) -> None:
        if self.value < 0:
            raise BadDogAgeException(str(self.value))

    @override
    def as_generic_type(self) -> int:
        return int(self.value)


@dataclass(frozen=True)
class Gender(BaseValueObject):
    value: str

    @override
    def validate(self) -> None:
        if self.value not in ("Male", "Female"):
            raise BadDogAgeException(str(self.value))

    @override
    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Color(BaseValueObject):
    value: str

    @override
    def validate(self) -> None:
        pattern: re.Pattern[str] = re.compile(r'^[A-Za-zА-Яа-яЁё]+(?:\s[A-Za-zА-Яа-яЁё]+)*$')

        if re.match(pattern, self.value) is None:
            raise BadDogColorException(self.value)

    @override
    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class FavouriteFood(BaseValueObject):
    value: str

    @override
    def validate(self) -> None:
        pattern: re.Pattern[str] = re.compile(r'^[A-Za-zА-Яа-яЁё]+(?:\s[A-Za-zА-Яа-яЁё]+)*$')

        if re.match(pattern, self.value) is None:
            raise BadDogFavouriteFoodException(self.value)

    @override
    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class FavouriteToy(BaseValueObject):
    value: str

    @override
    def validate(self) -> None:
        pattern: re.Pattern[str] = re.compile(r'^[A-Za-zА-Яа-яЁё]+(?:\s[A-Za-zА-Яа-яЁё]+)*$')

        if re.match(pattern, self.value) is None:
            raise BadDogFavouriteToyException(self.value)

    @override
    def as_generic_type(self) -> str:
        return str(self.value)

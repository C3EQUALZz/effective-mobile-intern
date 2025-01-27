import re
from dataclasses import dataclass
from typing import override

from dogs.domain.values.base import BaseValueObject
from dogs.exceptions.domain import BadNameException


@dataclass(frozen=True)
class Name(BaseValueObject):
    """
    Value object that represents a name of a dog or name of a breed.
    It must be not blank and doesn't have any special characters such as digits, "_" and etc.
    """
    value: str

    @override
    def validate(self) -> None:
        pattern: re.Pattern[str] = re.compile(r'^[A-Za-zА-Яа-яЁё]+(?:\s[A-Za-zА-Яа-яЁё]+)*$')

        if re.match(pattern, self.value) is None:
            raise BadNameException(self.value)

    @override
    def as_generic_type(self) -> str:
        return str(self.value)

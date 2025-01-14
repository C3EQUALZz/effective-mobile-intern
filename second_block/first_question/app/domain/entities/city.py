from dataclasses import dataclass
from datetime import datetime

from typing_extensions import override

from app.domain.entities.base import BaseEntity


@dataclass(eq=False, slots=True)
class City(BaseEntity):
    name: str
    days_delivery: datetime

    @override
    def __hash__(self) -> int:
        return hash(self.__slots__[1:])

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            raise NotImplementedError
        return self.__slots__[1:] == other.__slots__[1:]

from dataclasses import dataclass
from typing import override

from app.domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Author(BaseValueObject[str]):
    name: str

    @override
    def validate(self) -> str:
        ...

    @override
    def as_generic_type(self) -> str:
        return str(self.name)

from dataclasses import dataclass

from dogs.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class CreateDogCommand(AbstractCommand):
    breed_oid: str
    name: str
    age: int
    gender: str
    color: str
    favourite_food: str
    favourite_toy: str

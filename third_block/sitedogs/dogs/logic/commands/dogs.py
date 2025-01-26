from dataclasses import dataclass

from dogs.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class CreateDogCommand(AbstractCommand):
    breed_id: str
    name: str
    age: int
    gender: str
    color: str
    favorite_food: str
    favorite_toy: str

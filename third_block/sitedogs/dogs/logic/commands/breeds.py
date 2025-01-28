from dataclasses import dataclass

from core.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class CreateBreedCommand(AbstractCommand):
    name: str
    size: str
    friendliness: int
    train_ability: int
    shedding_amount: int
    exercise_needs: int


@dataclass(frozen=True)
class GetAllBreedsWithCountOfDogsForEachBreedCommand(AbstractCommand):
    page_number: int
    page_size: int


@dataclass(frozen=True)
class GetBreedByOid(AbstractCommand):
    breed_oid: str


@dataclass(frozen=True)
class DeleteBreedCommand(AbstractCommand):
    breed_oid: str


@dataclass(frozen=True)
class UpdateBreedCommand(AbstractCommand):
    breed_oid: str
    name: str
    size: str
    friendliness: int
    train_ability: int
    shedding_amount: int
    exercise_needs: int

from dataclasses import dataclass

from dogs.domain.entities.breed import BreedEntity


@dataclass(frozen=True)
class BreedWithCountOfDogs:
    breed: BreedEntity
    count: int

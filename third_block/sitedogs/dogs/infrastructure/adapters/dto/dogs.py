from dataclasses import dataclass

from dogs.domain.entities.dogs import DogEntity


@dataclass(frozen=True)
class DogsWithAverageAgeForEachBreed:
    dogs: list[DogEntity]
    average_age: float
    breed_name: str

from typing import (
    List,
    Optional,
    overload,
)

from dogs.domain.entities.dogs import DogEntity
from dogs.exceptions.infrastructure import DogNotFoundException
from dogs.infrastructure.adapters.dto.dogs import DogsWithAverageAgeForEachBreed
from dogs.infrastructure.repositories.dogs.base import DogsRepository


class DogsService:
    def __init__(self, repository: DogsRepository) -> None:
        self._repository = repository

    def get(self, dog_oid: str) -> DogEntity:
        existing_dog: Optional[DogEntity] = self._repository.get(oid=dog_oid)

        if existing_dog is None:
            raise DogNotFoundException(f"oid {dog_oid}")

        return existing_dog

    def add(self, dog: DogEntity) -> DogEntity:
        return self._repository.add(dog)

    def update(self, dog: DogEntity) -> DogEntity:
        existing_dog: Optional[DogEntity] = self._repository.get(oid=dog.oid)

        if existing_dog is None:
            raise DogNotFoundException(f"oid {dog.oid}")

        return self._repository.update(oid=existing_dog.oid, model=dog)

    def delete(self, dog_oid: str) -> None:
        existing_dog: Optional[DogEntity] = self._repository.get(oid=dog_oid)

        if existing_dog is None:
            raise DogNotFoundException(f"oid {dog_oid}")

        return self._repository.delete(dog_oid)

    def list_all_dogs_with_average_year(
        self, page_number: int = 0, page_size: int = 10
    ) -> List[DogsWithAverageAgeForEachBreed]:
        start: int = (page_number - 1) * page_size
        limit: int = start + page_size

        return self._repository.list_dogs_with_average_age_for_each_breed(start=start, limit=limit)

    @overload
    def check_existence(self, dog_id: str) -> bool: ...

    @overload
    def check_existence(self, name: str, age: int, gender: str) -> bool: ...

    def check_existence(self, *args) -> bool:
        match len(args):
            case 1:
                return self.get(args[0]) is not None
            case 3:
                name, age, gender = args
                if self._repository.get_by_name_age_gender(name=name, age=age, gender=gender):
                    return True
            case _:
                return False

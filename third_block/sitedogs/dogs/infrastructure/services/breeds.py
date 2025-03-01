
from dogs.domain.entities.breed import BreedEntity
from dogs.exceptions.infrastructure import BreedNotFoundException
from dogs.infrastructure.adapters.dto.breeds import BreedWithCountOfDogs
from dogs.infrastructure.repositories.breeds.base import BreedsRepository


class BreedsService:
    def __init__(self, breeds_repository: BreedsRepository) -> None:
        self._repository = breeds_repository

    def add(self, breed: BreedEntity) -> BreedEntity:
        return self._repository.add(breed)

    def get(self, breed_oid: str) -> BreedEntity:
        breed: BreedEntity | None = self._repository.get(breed_oid)

        if breed is None:
            raise BreedNotFoundException(f"oid {breed_oid}")

        return breed

    def update(self, breed: BreedEntity) -> BreedEntity:
        existing_breed: BreedEntity | None = self._repository.get(breed.oid)

        if existing_breed is None:
            raise BreedNotFoundException(f"oid {breed.oid}")

        return self._repository.update(existing_breed.oid, breed)

    def list_all_breeds_with_count_of_dogs_for_each_breed(
        self, page_number: int, page_size: int
    ) -> list[BreedWithCountOfDogs]:
        start: int = (page_number - 1) * page_size
        limit: int = start + page_size

        return self._repository.list_with_count_for_each_breed(start, limit)

    def delete(self, breed_oid: str) -> None:
        breed: BreedEntity | None = self._repository.get(breed_oid)

        if breed is None:
            raise BreedNotFoundException(f"oid {breed_oid}")

        return self._repository.delete(breed_oid)

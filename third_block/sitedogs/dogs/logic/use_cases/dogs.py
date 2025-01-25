from dogs.domain.entities.dogs import DogEntity
from dogs.infrastructure.adapters.dto.dogs import DogsWithAverageAgeForEachBreed
from dogs.infrastructure.repositories.dogs.base import DogsRepository
from dogs.infrastructure.services.dogs import DogsService


class CreateDogUseCase:
    def __init__(self, repository: DogsRepository) -> None:
        self._service = DogsService(repository)

    def execute(self, dog: DogEntity) -> DogEntity:
        return self._service.add(dog)


class UpdateDogUseCase:
    def __init__(self, repository: DogsRepository) -> None:
        self._service = DogsService(repository)

    def execute(self, dog: DogEntity) -> DogEntity:
        return self._service.update(dog)


class DeleteDogUseCase:
    def __init__(self, repository: DogsRepository) -> None:
        self._service = DogsService(repository)

    def execute(self, dog_oid: str) -> None:
        return self._service.delete(dog_oid)


class GetAllDogsWithAverageYearUseCase:
    def __init__(self, repository: DogsRepository) -> None:
        self._service = DogsService(repository)

    def execute(self, page_number: int, page_size: int) -> list[DogsWithAverageAgeForEachBreed]:
        return self._service.list_all_dogs_with_average_year(page_number, page_size)


class GetDogByOidWithNumberOfSameBreedUseCase:
    def __init__(self, repository: DogsRepository) -> None:
        self._service = DogsService(repository)

    def execute(self, dog_oid: str) -> DogEntity:
        ...

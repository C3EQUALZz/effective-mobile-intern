from dogs.domain.entities.breed import BreedEntity
from dogs.domain.entities.dogs import DogEntity
from dogs.domain.values.dog import (
    Age,
    Color,
    FavouriteFood,
    FavouriteToy,
    Gender,
)
from dogs.domain.values.shared import Name
from dogs.infrastructure.adapters.dto.dogs import DogsWithAverageAgeForEachBreed
from dogs.infrastructure.repositories.breeds.base import BreedsRepository
from dogs.infrastructure.repositories.dogs.base import DogsRepository
from dogs.infrastructure.services.breeds import BreedsService
from dogs.infrastructure.services.dogs import DogsService
from dogs.logic.commands.dogs import (
    CreateDogCommand,
    DeleteDogCommand,
    UpdateDogCommand,
)


class CreateDogUseCase:
    def __init__(self, dogs_repository: DogsRepository, breed_repository: BreedsRepository) -> None:
        self._dogs_service = DogsService(dogs_repository)
        self._breed_service = BreedsService(breed_repository)

    def execute(self, command: CreateDogCommand) -> DogEntity:
        breed: BreedEntity = self._breed_service.get(command.breed_oid)

        dog: DogEntity = DogEntity(
            name=Name(command.name),
            age=Age(command.age),
            gender=Gender(command.gender),
            color=Color(command.color),
            favorite_food=FavouriteFood(command.favourite_food),
            favorite_toy=FavouriteToy(command.favourite_toy),
            breed=breed,
        )

        return self._dogs_service.add(dog)


class UpdateDogUseCase:
    def __init__(
        self,
        dog_repository: DogsRepository,
        breed_repository: BreedsRepository,
    ) -> None:
        self._dog_service = DogsService(dog_repository)
        self._breed_service = BreedsService(breed_repository)

    def execute(self, command: UpdateDogCommand) -> DogEntity:
        breed_entity: BreedEntity = self._breed_service.get(command.breed_oid)

        dog: DogEntity = DogEntity(
            oid=command.oid,
            name=Name(command.name),
            age=Age(command.age),
            gender=Gender(command.gender),
            color=Color(command.color),
            favorite_food=FavouriteFood(command.favourite_food),
            favorite_toy=FavouriteToy(command.favourite_toy),
            breed=breed_entity,
        )

        self._dog_service.check_existence(
            dog.name.as_generic_type(),
            dog.age.as_generic_type(),
            dog.gender.as_generic_type(),
        )

        return self._dog_service.update(dog)


class DeleteDogUseCase:
    def __init__(self, repository: DogsRepository) -> None:
        self._service = DogsService(repository)

    def execute(self, command: DeleteDogCommand) -> None:
        return self._service.delete(command.oid)


class GetAllDogsWithAverageAgeForEachBreedUseCase:
    def __init__(self, repository: DogsRepository) -> None:
        self._service = DogsService(repository)

    def execute(self, page_number: int, page_size: int) -> list[DogsWithAverageAgeForEachBreed]:
        return self._service.list_all_dogs_with_average_year(page_number, page_size)


class GetDogByOidWithNumberOfSameBreedUseCase:
    def __init__(self, repository: DogsRepository) -> None:
        self._service = DogsService(repository)

    def execute(self, dog_oid: str) -> DogEntity:
        return self._service.get(dog_oid)

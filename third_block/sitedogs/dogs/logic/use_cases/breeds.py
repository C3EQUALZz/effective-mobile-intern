from dogs.domain.entities.breed import BreedEntity
from dogs.domain.values.breed import Size, Friendliness, TrainAbility, SheddingAmount, ExerciseNeeds
from dogs.domain.values.shared import Name
from dogs.infrastructure.adapters.dto.breeds import BreedWithCountOfDogs
from dogs.infrastructure.repositories.breeds.base import BreedsRepository
from dogs.infrastructure.services.breeds import BreedsService
from dogs.logic.commands.breeds import CreateBreedCommand, DeleteBreedCommand, \
    GetAllBreedsWithCountOfDogsForEachBreedCommand, GetBreedByOid, UpdateBreedCommand


class CreateBreedUseCase:
    def __init__(self, repository: BreedsRepository) -> None:
        self._service = BreedsService(repository)

    def execute(self, command: CreateBreedCommand) -> BreedEntity:
        breed: BreedEntity = BreedEntity(
            name=Name(command.name),
            size=Size(command.size),
            friendliness=Friendliness(command.friendliness),
            train_ability=TrainAbility(command.train_ability),
            shedding_amount=SheddingAmount(command.shedding_amount),
            exercise_needs=ExerciseNeeds(command.exercise_needs),
        )

        return self._service.add(breed)


class GetBreedByOidUseCase:
    def __init__(self, repository: BreedsRepository) -> None:
        self._service = BreedsService(repository)

    def execute(self, command: GetBreedByOid) -> BreedEntity:
        return self._service.get(command.breed_oid)


class UpdateBreedUseCase:
    def __init__(self, repository: BreedsRepository) -> None:
        self._service = BreedsService(repository)

    def execute(self, command: UpdateBreedCommand) -> BreedEntity:
        ...


class GetAllBreedsWithCountOfDogsForEachBreedUseCase:
    def __init__(self, repository: BreedsRepository) -> None:
        self._service = BreedsService(repository)

    def execute(self, command: GetAllBreedsWithCountOfDogsForEachBreedCommand) -> list[BreedWithCountOfDogs]:
        return self._service.list_all_breeds_with_count_of_dogs_for_each_breed(
            command.page_number,
            command.page_size,
        )


class DeleteBreedUseCase:
    def __init__(self, repository: BreedsRepository) -> None:
        self._service = BreedsService(repository)

    def execute(self, command: DeleteBreedCommand) -> None:
        return self._service.delete(breed_oid=command.breed_oid)

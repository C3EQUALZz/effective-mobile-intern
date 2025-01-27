import anydi
from dogs.infrastructure.adapters.django_orm.breeds import BreedsAdapter
from dogs.infrastructure.adapters.django_orm.dogs import DogsAdapter
from dogs.infrastructure.repositories.breeds.base import BreedsRepository
from dogs.infrastructure.repositories.breeds.django_orm import DjangoORMBreedsRepository
from dogs.infrastructure.repositories.dogs.base import DogsRepository
from dogs.infrastructure.repositories.dogs.django_orm import DjangoORMDogsRepository
from dogs.logic.use_cases.breeds import (
    CreateBreedUseCase,
    DeleteBreedUseCase,
    GetAllBreedsWithCountOfDogsForEachBreedUseCase,
    GetBreedByOidUseCase,
    UpdateBreedUseCase,
)
from dogs.logic.use_cases.dogs import (
    CreateDogUseCase,
    DeleteDogUseCase,
    GetAllDogsWithAverageAgeForEachBreedUseCase,
    GetDogByOidWithNumberOfSameBreedUseCase,
    UpdateDogUseCase,
)


class DogsModule(anydi.Module):
    @anydi.provider(scope="singleton")
    def dogs_repository(self) -> DogsRepository:
        return DjangoORMDogsRepository(DogsAdapter())

    @anydi.provider(scope="singleton")
    def dogs_create_use_case(self, dog_repo: DogsRepository, breed_repo: BreedsRepository) -> CreateDogUseCase:
        return CreateDogUseCase(dog_repo, breed_repo)

    @anydi.provider(scope="singleton")
    def dogs_update_use_case(self, repo: DogsRepository, breed_repo: BreedsRepository) -> UpdateDogUseCase:
        return UpdateDogUseCase(repo, breed_repo)

    @anydi.provider(scope="singleton")
    def dogs_delete_use_case(self, repo: DogsRepository) -> DeleteDogUseCase:
        return DeleteDogUseCase(repo)

    @anydi.provider(scope="singleton")
    def dogs_get_all_dogs_with_average_year_use_case(
            self,
            repo: DogsRepository
    ) -> GetAllDogsWithAverageAgeForEachBreedUseCase:
        return GetAllDogsWithAverageAgeForEachBreedUseCase(repo)

    @anydi.provider(scope="singleton")
    def dogs_get_dog_by_oid_with_number_of_same_breed_use_case(
            self,
            repo: DogsRepository
    ) -> GetDogByOidWithNumberOfSameBreedUseCase:
        return GetDogByOidWithNumberOfSameBreedUseCase(repo)


class BreedsModule(anydi.Module):
    @anydi.provider(scope="singleton")
    def breeds_repository(self) -> BreedsRepository:
        return DjangoORMBreedsRepository(BreedsAdapter())

    @anydi.provider(scope="singleton")
    def breeds_create_use_case(self, repo: BreedsRepository) -> CreateBreedUseCase:
        return CreateBreedUseCase(repo)

    @anydi.provider(scope="singleton")
    def breed_get_by_oid_use_case(self, repo: BreedsRepository) -> GetBreedByOidUseCase:
        return GetBreedByOidUseCase(repo)

    @anydi.provider(scope="singleton")
    def breed_update_use_case(self, repo: BreedsRepository) -> UpdateBreedUseCase:
        return UpdateBreedUseCase(repo)

    @anydi.provider(scope="singleton")
    def breed_delete_use_case(self, repo: BreedsRepository) -> DeleteBreedUseCase:
        return DeleteBreedUseCase(repo)

    @anydi.provider(scope="singleton")
    def breed_get_all_breeds_with_count_of_dogs_use_case(
            self,
            repo: BreedsRepository
    ) -> GetAllBreedsWithCountOfDogsForEachBreedUseCase:
        return GetAllBreedsWithCountOfDogsForEachBreedUseCase(repo)

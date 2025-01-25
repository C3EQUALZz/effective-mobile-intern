import anydi

from dogs.infrastructure.adapters.django_orm.dogs import DogsAdapter
from dogs.infrastructure.repositories.dogs.base import DogsRepository
from dogs.infrastructure.repositories.dogs.django_orm import DjangoORMDogsRepository
from dogs.logic.use_cases.dogs import CreateDogUseCase, DeleteDogUseCase, UpdateDogUseCase, \
    GetAllDogsWithAverageYearUseCase, GetDogByOidWithNumberOfSameBreedUseCase


class DogsModule(anydi.Module):
    @anydi.provider(scope="singleton")
    def dogs_repository(self) -> DogsRepository:
        return DjangoORMDogsRepository(DogsAdapter())

    @anydi.provider(scope="singleton")
    def dogs_create_use_case(self, repo: DogsRepository) -> CreateDogUseCase:
        return CreateDogUseCase(repo)

    @anydi.provider(scope="singleton")
    def dogs_update_use_case(self, repo: DogsRepository) -> UpdateDogUseCase:
        return UpdateDogUseCase(repo)

    @anydi.provider(scope="singleton")
    def dogs_delete_use_case(self, repo: DogsRepository) -> DeleteDogUseCase:
        return DeleteDogUseCase(repo)

    @anydi.provider(scope="singleton")
    def dogs_get_all_dogs_with_average_year_use_case(self, repo: DogsRepository) -> GetAllDogsWithAverageYearUseCase:
        return GetAllDogsWithAverageYearUseCase(repo)

    @anydi.provider(scope="singleton")
    def dogs_get_dog_by_oid_with_number_of_same_breed_use_case(
            self,
            repo: DogsRepository
    ) -> GetDogByOidWithNumberOfSameBreedUseCase:
        return GetDogByOidWithNumberOfSameBreedUseCase(repo)

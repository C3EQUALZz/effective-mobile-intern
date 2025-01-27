from typing import List, Optional, override

from django.db.models import Count

from dogs.domain.entities.breed import BreedEntity
from dogs.infrastructure.adapters.django_orm.orm import Breed
from dogs.infrastructure.adapters.dto.breeds import BreedWithCountOfDogs
from dogs.infrastructure.repositories.breeds.base import BreedsRepository


class DjangoORMBreedsRepository(BreedsRepository):
    @override
    def add(self, model: BreedEntity) -> BreedEntity:
        breed_model = self._adapter.to_model(model)
        breed_model.save()
        return model

    @override
    def get(self, oid: str) -> Optional[BreedEntity]:
        breed: Optional[Breed] = Breed.objects.get(oid=oid)
        return None if breed is None else self._adapter.to_entity(breed)

    @override
    def update(self, oid: str, model: BreedEntity) -> BreedEntity:
        Breed.objects.filter(oid=oid).update(**model.to_dict(exclude={"oid"}))
        return self._adapter.to_entity(Breed.objects.get(oid=oid))

    @override
    def list(self, start: int = 0, limit: int = 10) -> List[BreedEntity]:
        return [self._adapter.to_entity(breed) for breed in Breed.objects.all()[start:start + limit]]

    @override
    def delete(self, oid: str) -> None:
        Breed.objects.get(oid=oid).delete()

    @override
    def list_with_count_for_each_breed(self, start: int = 0, limit: int = 10) -> List[BreedWithCountOfDogs]:
        breeds_with_counts = (
            Breed.objects.annotate(dog_count=Count('dogs'))
            [start:start + limit]
        )

        return [
            BreedWithCountOfDogs(
                breed=self._adapter.to_entity(breed),
                count=breed.dog_count  # type: ignore
            )
            for breed in breeds_with_counts
        ]

from typing import (
    List,
    Literal,
    Optional,
    override,
)

from django.db.models import (
    Avg,
    OuterRef,
    Subquery,
)

from dogs.domain.entities.dogs import DogEntity
from dogs.infrastructure.adapters.django_orm.orm import (
    Breed,
    Dog,
)
from dogs.infrastructure.adapters.dto.dogs import DogsWithAverageAgeForEachBreed
from dogs.infrastructure.repositories.dogs.base import DogsRepository


class DjangoORMDogsRepository(DogsRepository):
    @override
    def get_by_name_age_gender(self, name: str, age: int, gender: Literal["Male", "Female"]) -> List[DogEntity]:
        dogs = Dog.objects.filter(name=name, age=age, gender=gender)
        return [self._adapter.to_entity(dog) for dog in dogs]

    @override
    def add(self, model: DogEntity) -> DogEntity:
        dog_model: Dog = self._adapter.to_model(model)
        dog_model.save()
        return model

    @override
    def get(self, oid: str) -> Optional[DogEntity]:
        dog: Optional[Dog] = Dog.objects.get(oid=oid)
        return None if dog is None else self._adapter.to_entity(dog)

    @override
    def delete(self, oid: str) -> None:
        Dog.objects.get(oid=oid).delete()

    @override
    def update(self, oid: str, model: DogEntity) -> DogEntity:
        new_dog: Dog = self._adapter.to_model(model)

        Dog.objects.filter(oid=oid).update(
            name=new_dog.name,
            age=new_dog.age,
            gender=new_dog.gender,
            breed=new_dog.breed,
            color=new_dog.color,
            favorite_food=new_dog.favorite_food,
            favorite_toy=new_dog.favorite_toy
        )

        return self.get(oid)

    @override
    def list(self, start: int = 0, limit: int = 10) -> List[DogEntity]:
        return [self._adapter.to_entity(dog) for dog in Dog.objects.all()[start:limit]]

    @override
    def list_dogs_with_average_age_for_each_breed(
            self,
            start: int = 0,
            limit: int = 10
    ) -> List[DogsWithAverageAgeForEachBreed]:
        # Получаем породы с их средним возрастом
        breeds_with_avg_age = Breed.objects.annotate(
            avg_age=Subquery(
                Dog.objects.filter(
                    breed=OuterRef('pk')
                ).values('breed').annotate(
                    avg_age=Avg('age')
                ).values('avg_age')[:1]
            )
        )[start:limit]

        result: List[DogsWithAverageAgeForEachBreed] = [
            DogsWithAverageAgeForEachBreed(
                breed_name=breed.name,
                average_age=breed.avg_age or 0.0,  # type: ignore
                dogs=[self._adapter.to_entity(dog) for dog in breed.dogs.all()]
            )
            for breed in breeds_with_avg_age
        ]

        return result

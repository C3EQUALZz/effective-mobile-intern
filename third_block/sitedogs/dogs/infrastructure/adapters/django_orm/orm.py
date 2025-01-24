from django.db import models
from typing import Final


class Breed(models.Model):
    SIZE_CHOICES: Final[list[tuple[str, str]]] = [
        (size, size) for size in ['Tiny', 'Small', 'Medium', 'Large']
    ]

    oid = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=255, unique=True)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    friendliness = models.PositiveSmallIntegerField(default=1, choices=[(i, i) for i in range(1, 6)])
    train_ability = models.PositiveSmallIntegerField(default=1, choices=[(i, i) for i in range(1, 6)])
    shedding_amount = models.PositiveSmallIntegerField(default=1, choices=[(i, i) for i in range(1, 6)])
    exercise_needs = models.PositiveSmallIntegerField(default=1, choices=[(i, i) for i in range(1, 6)])

    def __str__(self) -> str:
        return self.name


class Dog(models.Model):
    GENDER_CHOICES: Final[list[tuple[str, str]]] = [
        (size, size) for size in ['Male', 'Female']
    ]

    oid = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, related_name='dogs')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    color = models.CharField(max_length=50)
    favorite_food = models.CharField(max_length=255, blank=True, null=True)
    favorite_toy = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.breed.name})"

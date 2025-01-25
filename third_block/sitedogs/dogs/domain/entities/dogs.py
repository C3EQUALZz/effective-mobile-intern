from dataclasses import dataclass

from dogs.domain.entities.base import BaseEntity
from dogs.domain.entities.breed import BreedEntity
from dogs.domain.values.dog import Age, Gender, Color, FavouriteFood, FavouriteToy
from dogs.domain.values.shared import Name


@dataclass(eq=False)
class DogEntity(BaseEntity):
    """
    Domain entity that represents a dog.
    It has several attributes:
    - name: Name of the dog. Must be a string that has only letters.
    - age: Age of the dog. Must be a positive integer.
    - gender: Gender of the dog. Must be a string that has only letters. Has two types: male, female.
    - breed: Breed of the dog. Check description in entity.
    - color: Color of the dog. Must be a string that has only letters.
    - favourite_food: Favourite food of the dog. Must be a string that has only letters.
    - favorite_toy: Favorite toy of the dog. Must be a string that has only letters.
    """
    name: Name
    age: Age
    breed: BreedEntity
    gender: Gender
    color: Color
    favorite_food: FavouriteFood
    favorite_toy: FavouriteToy

    __eq__ = BaseEntity.__eq__
    __hash__ = BaseEntity.__hash__

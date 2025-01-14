from dataclasses import dataclass
from decimal import Decimal

from app.domain.entities.base import BaseEntity
from app.domain.values.author import Author
from app.domain.values.book import Genre


@dataclass(eq=False, slots=True)
class Book(BaseEntity):
    title: str
    author: Author
    genre: Genre
    price: Decimal
    amount: int

    __hash__ = BaseEntity.__hash__
    __eq__ = BaseEntity.__eq__

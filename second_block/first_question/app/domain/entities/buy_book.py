from dataclasses import dataclass

from app.domain.entities.base import BaseEntity
from app.domain.entities.book import Book


@dataclass(eq=False, slots=True)
class BuyBook(BaseEntity):
    book: Book
    amount: int

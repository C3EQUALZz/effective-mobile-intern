from dataclasses import dataclass, field
from typing import List

from app.domain.entities.base import BaseEntity
from app.domain.entities.buy_book import BuyBook
from app.domain.entities.buy_step import BuyStep
from app.domain.entities.client import Client


@dataclass(eq=False, slots=True)
class Buy(BaseEntity):
    client: Client
    description: str
    books: List[BuyBook] = field(default_factory=list)
    steps: List[BuyStep] = field(default_factory=list)

    def add_book(self, book: BuyBook) -> None:
        """Добавить книгу в заказ"""
        self.books.append(book)

    def add_step(self, step: BuyStep) -> None:
        """Добавить шаг выполнения"""
        self.steps.append(step)

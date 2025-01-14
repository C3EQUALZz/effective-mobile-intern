from dataclasses import dataclass

from app.domain.entities.base import BaseEntity
from app.domain.entities.city import City


@dataclass(eq=False, slots=True)
class Client(BaseEntity):
    name: str
    city: City
    email: str

    __hash__ = BaseEntity.__hash__
    __eq__ = BaseEntity.__eq__

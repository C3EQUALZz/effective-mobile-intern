from typing import Literal

from sqlalchemy import Integer, TypeDecorator, Dialect

from app.domain.values.trading_result import Volume, Total, Count


class VolumeDecorator(TypeDecorator):
    impl = Integer
    cache_ok = True

    def process_bind_param(self, value: dict[Literal["value"], int], dialect: Dialect) -> int:
        if value is not None:
            return value["value"]

    def process_result_value(self, value: int, dialect: Dialect) -> Volume:
        if value is not None:
            return Volume(value)


class TotalDecorator(TypeDecorator):
    impl = Integer
    cache_ok = True

    def process_bind_param(self, money: dict[Literal["value"], int], dialect: Dialect) -> int:
        if money is not None:
            return money["value"]

    def process_result_value(self, value: int, dialect: Dialect) -> Total:
        if value is not None:
            return Total(value)


class CountDecorator(TypeDecorator):
    impl = Integer
    cache_ok = True

    def process_bind_param(self, value: dict[Literal["value"], int], dialect: Dialect) -> int:
        if value is not None:
            return value["value"]

    def process_result_value(self, value: int, dialect: Dialect) -> Count:
        if value is not None:
            return Count(value)

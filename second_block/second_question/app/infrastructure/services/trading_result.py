from datetime import date
from typing import Final, Optional, List

import pandas as pd

from app.domain.entities.trading_result import TradingResultEntity
from app.domain.values.trading_result import Total, Count, Volume
from app.infrastructure.exceptions import NoSuchTradingEntityException, AttributeException
from app.infrastructure.services.parsers.trading_result.spimex.base import AbstractSpimexParser
from app.infrastructure.uow.trading_result.base import TradingResultUnitOfWork

SELECTED_COLUMNS: Final[List[str]] = [
    'Код Инструмента',
    'Наименование Инструмента',
    'Базис поставки',
    'Объем Договоров в единицах измерения',
    'Обьем Договоров, руб.',
    'Количество Договоров, шт.'

]


class TradingResultService:
    def __init__(self, uow: TradingResultUnitOfWork) -> None:
        self._uow = uow

    async def get_by_exchange_product_id(self, exchange_product_id: str) -> TradingResultEntity:
        async with self._uow as uow:
            trading_result_entity: TradingResultEntity = await uow.products_market.get_by_exchange_product_id(
                exchange_product_id
            )

            if not trading_result_entity:
                raise NoSuchTradingEntityException(exchange_product_id)

            return trading_result_entity

    async def check_existence(
            self,
            oid: Optional[str] = None,
            exchange_product_id: Optional[str] = None,
    ) -> bool:

        if not (oid or exchange_product_id):
            raise AttributeException("oid or user_oid")

        async with self._uow as uow:
            score: TradingResultEntity

            if oid:
                score = await uow.products_market.get(oid=oid)
                if score:
                    return True

            if exchange_product_id:
                score = await uow.products_market.get_by_exchange_product_id(exchange_product_id)
                if score:
                    return True

        return False

    async def parse_and_add_to_database(self, parser: AbstractSpimexParser, start_date: date, end_date: date) -> None:
        async with self._uow as uow:
            generator_of_results = parser.parse(start_date=start_date, end_date=end_date)

            async for date_of_creation, file_content in generator_of_results:  # type: ignore

                df = pd.read_excel(file_content, skiprows=6).iloc[:-2, 1:]
                df.columns = df.columns.str.replace('\n', ' ')
                df = df[df['Код Инструмента'].notnull()]  # Убирает строки, где нет кода инструмента
                df['Количество Договоров, шт.'] = df['Количество Договоров, шт.'].replace('-', 0).astype(int)
                df = df[df['Количество Договоров, шт.'] > 0]
                df = df[SELECTED_COLUMNS]

                for _, row in df.iterrows():
                    trading_result = TradingResultEntity(
                        exchange_product_id=row["Код Инструмента"],
                        exchange_product_name=row["Наименование Инструмента"],
                        delivery_basis_name=row["Базис поставки"],
                        volume=Volume(int(row["Объем Договоров в единицах измерения"])),
                        total=Total(int(row["Обьем Договоров, руб."])),
                        count=Count(int(row["Количество Договоров, шт."])),
                        date=date_of_creation
                    )
                    await uow.products_market.add(trading_result)
            await uow.commit()

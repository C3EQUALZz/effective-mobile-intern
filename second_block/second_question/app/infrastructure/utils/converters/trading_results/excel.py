from datetime import date
from io import BytesIO
from typing import Final, AsyncGenerator

import pandas as pd

from app.domain.entities.trading_result import TradingResultEntity
from app.domain.values.trading_result import Volume, Total, Count
from app.infrastructure.utils.converters.trading_results.base import AbstractDocumentConverter

SELECTED_COLUMNS: Final[list[str]] = [
    "Код Инструмента",
    "Наименование Инструмента",
    "Базис поставки",
    "Объем Договоров в единицах измерения",
    "Обьем Договоров, руб.",
    "Количество Договоров, шт.",
]


class ExcelDocumentConverter(AbstractDocumentConverter):
    async def convert(self, file_content: BytesIO, date_of_creation: date) -> AsyncGenerator[TradingResultEntity, None]:
        df = pd.read_excel(file_content, skiprows=6).iloc[:-2, 1:]
        df.columns = df.columns.str.replace("\n", " ")
        df = df[df["Код Инструмента"].notnull()]  # Убирает строки, где нет кода инструмента
        df["Количество Договоров, шт."] = df["Количество Договоров, шт."].replace("-", 0).astype(int)
        df = df[df["Количество Договоров, шт."] > 0]
        df = df[SELECTED_COLUMNS]

        for _, row in df.iterrows():
            trading_result = TradingResultEntity(
                exchange_product_id=row["Код Инструмента"],
                exchange_product_name=row["Наименование Инструмента"],
                delivery_basis_name=row["Базис поставки"],
                volume=Volume(int(row["Объем Договоров в единицах измерения"])),
                total=Total(int(row["Обьем Договоров, руб."])),
                count=Count(int(row["Количество Договоров, шт."])),
                date=date_of_creation,
            )
            yield trading_result

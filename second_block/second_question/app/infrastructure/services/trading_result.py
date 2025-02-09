import logging
from datetime import date

from app.domain.entities.trading_result import TradingResultEntity
from app.exceptions.infrastructure import (
    AttributeException,
    NoSuchTradingEntityException,
)
from app.infrastructure.services.parsers.trading_result.spimex.base import AbstractSpimexParser
from app.infrastructure.uow.trading_result.base import TradingResultUnitOfWork
from app.infrastructure.utils.converters.trading_results.base import AbstractDocumentConverter

logger = logging.getLogger(__name__)


class TradingResultService:
    def __init__(self, uow: TradingResultUnitOfWork) -> None:
        self._uow = uow

    async def get_by_exchange_product_id(
            self,
            exchange_product_id: str,
            page_number: int,
            page_size: int
    ) -> list[TradingResultEntity]:

        start: int = (page_number - 1) * page_size
        limit: int = start + page_size

        async with self._uow as uow:
            trading_result_entity: list[TradingResultEntity] = await uow.products_market.get_by_exchange_product_id(
                exchange_product_id=exchange_product_id,
                start=start,
                limit=limit,
            )

            if not trading_result_entity:
                raise NoSuchTradingEntityException(exchange_product_id)

            return trading_result_entity

    async def get_by_exchange_product_name(
            self,
            exchange_product_name: str,
            page_number: int,
            page_size: int
    ) -> list[TradingResultEntity]:

        start: int = (page_number - 1) * page_size
        limit: int = start + page_size

        async with self._uow as uow:
            trading_result_entity: list[TradingResultEntity] = await uow.products_market.get_by_exchange_product_name(
                exchange_product_name,
                start=start,
                limit=limit,
            )

            if not trading_result_entity:
                raise NoSuchTradingEntityException(exchange_product_name)

            return trading_result_entity

    async def get_list_by_date_period(
            self,
            start_date: date,
            end_date: date,
            page_number: int,
            page_size: int
    ) -> list[TradingResultEntity]:

        start: int = (page_number - 1) * page_size
        limit: int = start + page_size

        async with self._uow as uow:
            trading_result_entities: list[TradingResultEntity] = await uow.products_market.list_by_date(
                start_date=start_date,
                end_date=end_date,
                start=start,
                limit=limit,
            )

            if not trading_result_entities:
                raise NoSuchTradingEntityException(f"by period {start_date} - {end_date}")

            return trading_result_entities

    async def check_existence(
            self,
            oid: str | None = None,
            exchange_product_id: str | None = None,
    ) -> bool:
        if not (oid or exchange_product_id):
            raise AttributeException("oid or exchange_product_id")

        async with self._uow as uow:
            score: TradingResultEntity | list[TradingResultEntity]

            if oid:
                score = await uow.products_market.get(oid=oid)
                if score:
                    return True

            if exchange_product_id:
                score = await uow.products_market.get_by_exchange_product_id(exchange_product_id, limit=1)
                if score:
                    return True

        return False

    async def parse_and_add_to_database(
            self,
            parser: AbstractSpimexParser,
            converter: AbstractDocumentConverter,
            start_date: date,
            end_date: date
    ) -> None:

        async with self._uow as uow:
            generator_of_results = parser.parse(start_date=start_date, end_date=end_date)

            async for date_of_creation, file_content in generator_of_results:  # type: ignore
                try:
                    async for trading_result in converter.convert(file_content, date_of_creation): # type: ignore
                        await uow.products_market.add(trading_result)
                except ValueError as e:
                    logger.error("Error while parsing data from pandas file: %s", e)
            await uow.commit()

from datetime import date

from app.domain.entities.trading_result import TradingResultEntity
from app.exceptions.infrastructure import NoSuchTradingEntityException
from app.infrastructure.services.parsers.trading_result.spimex.browser_automation.all_bulletins import (
    SpimexAllBulletinsParser,
)
from app.infrastructure.services.trading_result import TradingResultService
from app.infrastructure.utils.converters.trading_results.excel import ExcelDocumentConverter
from app.infrastructure.utils.fetchers.aio_http import AiohttpFetcher
from app.logic.commands.trading_result import (
    GetByExchangeProductId,
    GetListOfTradesForSpecifiedPeriod,
    ParseAllBulletinsFromSphinx, GetLastTradingDates,
)
from app.logic.handlers.trading_result.base import TradingResultCommandHandler


class ParseAllBulletinsFromSphinxCommandHandler(TradingResultCommandHandler[ParseAllBulletinsFromSphinx]):
    async def __call__(self, command: ParseAllBulletinsFromSphinx) -> None:
        trading_result_service: TradingResultService = TradingResultService(self._uow)
        parser: SpimexAllBulletinsParser = SpimexAllBulletinsParser(AiohttpFetcher())
        converter: ExcelDocumentConverter = ExcelDocumentConverter()
        await trading_result_service.parse_and_add_to_database(parser, converter, command.start_date, command.end_date)


class GetByExchangeProductIdCommandHandler(TradingResultCommandHandler[GetByExchangeProductId]):
    async def __call__(self, command: GetByExchangeProductId) -> list[TradingResultEntity]:
        trading_result_service: TradingResultService = TradingResultService(self._uow)

        if not await trading_result_service.check_existence(exchange_product_id=command.exchange_product_id):
            raise NoSuchTradingEntityException(command.exchange_product_id)

        return await trading_result_service.get_by_exchange_product_id(
            exchange_product_id=command.exchange_product_id,
            page_size=command.page_size,
            page_number=command.page_number,
        )


class GetListOfTradesForSpecifiedPeriodCommandHandler(TradingResultCommandHandler[GetListOfTradesForSpecifiedPeriod]):
    async def __call__(self, command: GetListOfTradesForSpecifiedPeriod) -> list[TradingResultEntity]:
        trading_result_service: TradingResultService = TradingResultService(self._uow)

        trading_result_entities: list[TradingResultEntity] = await trading_result_service.get_list_by_date_period(
            start_date=command.start_date,
            end_date=command.end_date,
            page_number=command.page_number,
            page_size=command.page_size
        )

        if not trading_result_entities:
            raise NoSuchTradingEntityException(f"by period {command.start_date} - {command.end_date}")

        return trading_result_entities


class GetTradingResultByDayCommandHandler(TradingResultCommandHandler[GetLastTradingDates]):
    async def __call__(self, command: GetLastTradingDates) -> list[date]:
        trading_result_service: TradingResultService = TradingResultService(self._uow)

        trading_result_service.get_list_by_date_period()

from app.domain.entities.trading_result import TradingResultEntity
from app.infrastructure.exceptions import NoSuchTradingEntityException
from app.infrastructure.services.parsers.trading_result.spimex.browser_automation.all_bulletins import \
    SpimexAllBulletinsParser
from app.infrastructure.services.trading_result import TradingResultService
from app.infrastructure.utils.fetchers.aio_http import AiohttpFetcher
from app.logic.commands.trading_result import ParseAllBulletinsFromSphinx, GetByExchangeProductId
from app.logic.handlers.trading_result.base import TradingResultCommandHandler


class ParseAllBulletinsFromSphinxCommandHandler(TradingResultCommandHandler[ParseAllBulletinsFromSphinx]):
    async def __call__(self, command: ParseAllBulletinsFromSphinx) -> None:
        trading_result_service: TradingResultService = TradingResultService(self._uow)
        parser: SpimexAllBulletinsParser = SpimexAllBulletinsParser(AiohttpFetcher())
        await trading_result_service.parse_and_add_to_database(parser, command.start_date, command.end_date)


class GetGetByExchangeProductIdCommandHandler(TradingResultCommandHandler[GetByExchangeProductId]):
    async def __call__(self, command: GetByExchangeProductId) -> TradingResultEntity:
        trading_result_service: TradingResultService = TradingResultService(self._uow)

        if not await trading_result_service.check_existence(exchange_product_id=command.exchange_product_id):
            raise NoSuchTradingEntityException(command.exchange_product_id)

        return await trading_result_service.get_by_exchange_product_id(command.exchange_product_id)

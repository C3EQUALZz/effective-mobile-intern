from infrastructure.services.parsers.trading_result.spimex.browser_automation.all_bulletins import \
    SpimexAllBulletinsParser
from infrastructure.services.trading_result import TradingResultService
from infrastructure.utils.fetchers.aio_http import AiohttpFetcher
from logic.commands.trading_result import ParseAllBulletinsFromSphinx
from logic.handlers.trading_result.base import TradingResultCommandHandler


class ParseAllBulletinsFromSphinxCommandHandler(TradingResultCommandHandler[ParseAllBulletinsFromSphinx]):
    async def __call__(self, command: ParseAllBulletinsFromSphinx) -> None:
        trading_result_service: TradingResultService = TradingResultService(self._uow)
        parser: SpimexAllBulletinsParser = SpimexAllBulletinsParser(AiohttpFetcher())
        await trading_result_service.parse_and_add_to_database(parser, command.start_date, command.end_date)

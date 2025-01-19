from dishka.integrations.faststream import FromDishka
from faststream.kafka import KafkaRouter

from application.consumers.trading_result.schemas import ParseAllBulletinsSphinxRequest
from infrastructure.uow.trading_result.base import TradingResultUnitOfWork
from logic.bootstrap import Bootstrap, EventHandlerMapping, CommandHandlerMapping
from logic.commands.trading_result import ParseAllBulletinsFromSphinx
from logic.message_bus import MessageBus

router = KafkaRouter(
    prefix="spimex"
)


@router.subscriber("parse_sphinx")
async def parse_all_bulletins_from_sphinx(
        msg: ParseAllBulletinsSphinxRequest,
        uow: FromDishka[TradingResultUnitOfWork],
        events: FromDishka[EventHandlerMapping],
        commands: FromDishka[CommandHandlerMapping]
) -> None:
    bootstrap: Bootstrap = Bootstrap(
        uow=uow,
        events_handlers_for_injection=events,
        commands_handlers_for_injection=commands
    )

    messagebus: MessageBus = await bootstrap.get_messagebus()

    await messagebus.handle(ParseAllBulletinsFromSphinx(**msg.model_dump()))

    return messagebus.command_result

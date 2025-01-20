from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from app.application.api.trading_result.schemas import ParseAllBulletinsSphinxRequest
from app.infrastructure.uow.trading_result.base import TradingResultUnitOfWork
from app.logic.bootstrap import EventHandlerMapping, CommandHandlerMapping, Bootstrap
from app.logic.commands.trading_result import ParseAllBulletinsFromSphinx, GetByExchangeProductId
from app.logic.message_bus import MessageBus

router = APIRouter(
    prefix="/trading_result",
    tags=["trading_result"],
    route_class=DishkaRoute
)


@router.get("/last-trading-dates")
async def get_last_trading_dates():
    ...


@router.get("/last-trading-result")
async def get_last_trading_result():
    ...


@router.get("/{exchange_product_id}")
async def get_product_by_exchange_product_id(
        exchange_product_id: str,
        uow: FromDishka[TradingResultUnitOfWork],
        events: FromDishka[EventHandlerMapping],
        commands: FromDishka[CommandHandlerMapping]
):
    bootstrap: Bootstrap = Bootstrap(
        uow=uow,
        events_handlers_for_injection=events,
        commands_handlers_for_injection=commands
    )

    messagebus: MessageBus = await bootstrap.get_messagebus()

    await messagebus.handle(GetByExchangeProductId(exchange_product_id))

    return messagebus.command_result


@router.post("parse")
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

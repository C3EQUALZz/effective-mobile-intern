import logging
from datetime import (
    date,
    datetime,
)

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import (
    APIRouter,
    HTTPException,
    Query
)

from app.application.api.trading_result.schemas import (
    ParseAllBulletinsSpimexRequest,
    TradingResultsSpimexRequest,
)
from app.exceptions.base import ApplicationException
from app.infrastructure.uow.trading_result.base import TradingResultUnitOfWork
from app.logic.bootstrap import (
    Bootstrap,
    CommandHandlerMapping,
    EventHandlerMapping,
)
from app.logic.commands.trading_result import (
    GetByExchangeProductId,
    GetLastTradingDates,
    GetListOfTradesForSpecifiedPeriod,
    ParseAllBulletinsFromSphinx,
)
from app.logic.message_bus import MessageBus
from typing import Optional

router = APIRouter(prefix="/trading_result", tags=["trading_result"], route_class=DishkaRoute)

logger = logging.getLogger(__name__)


@router.get("/last-trading-dates/{count_of_days}")
async def get_last_trading_dates(
        uow: FromDishka[TradingResultUnitOfWork],
        events: FromDishka[EventHandlerMapping],
        commands: FromDishka[CommandHandlerMapping],
        count_of_days: int,
        page: int = Query(1, ge=1, description="Номер страницы"),
        size: int = Query(10, ge=1, le=100, description="Размер страницы")
) -> list[date]:
    try:
        bootstrap: Bootstrap = Bootstrap(
            uow=uow, events_handlers_for_injection=events, commands_handlers_for_injection=commands
        )

        messagebus: MessageBus = await bootstrap.get_messagebus()

        await messagebus.handle(GetLastTradingDates(
            count_of_days=count_of_days,
            page_number=page,
            page_size=size
        ))

        return messagebus.command_result

    except ApplicationException as e:
        logger.error(e.message)
        raise HTTPException(status_code=e.status, detail=e.message)


@router.get("/last-trading-result")
async def get_trading_results(
        uow: FromDishka[TradingResultUnitOfWork],
        events: FromDishka[EventHandlerMapping],
        commands: FromDishka[CommandHandlerMapping],
        oil_id: Optional[str] = Query(max_length=4),
        delivery_type_id: Optional[str] = Query(max_length=1, default=None),
        delivery_basis_id: Optional[str] = Query(max_length=3, default=None),
        start_date: date = date.today(),
        end_date: date = date.today(),
        page_number: int = Query(1, ge=1, description="Номер страницы"),
        page_size: int = Query(10, ge=1, le=100, description="Размер страницы")
) -> list[TradingResultsSpimexRequest]:
    try:
        bootstrap: Bootstrap = Bootstrap(
            uow=uow, events_handlers_for_injection=events, commands_handlers_for_injection=commands
        )

        messagebus: MessageBus = await bootstrap.get_messagebus()

        # await messagebus.handle(GetLastTradingDates(
        #     count_of_days=count_of_days,
        #     page_number=page,
        #     page_size=size
        # ))

        return messagebus.command_result

    except ApplicationException as e:
        logger.error(e.message)
        raise HTTPException(status_code=e.status, detail=e.message)


@router.get("/dynamics/{start_date}&{end_date}")
async def get_dynamics(
        uow: FromDishka[TradingResultUnitOfWork],
        events: FromDishka[EventHandlerMapping],
        commands: FromDishka[CommandHandlerMapping],
        start_date: date = datetime.now().date(),
        end_date: date = datetime.now().date(),
        page_number: int = Query(1, ge=1, description="Номер страницы"),
        page_size: int = Query(10, ge=1, le=100, description="Размер страницы"),
) -> list[TradingResultsSpimexRequest]:
    try:
        bootstrap: Bootstrap = Bootstrap(
            uow=uow, events_handlers_for_injection=events, commands_handlers_for_injection=commands
        )

        messagebus: MessageBus = await bootstrap.get_messagebus()

        await messagebus.handle(GetListOfTradesForSpecifiedPeriod(
            start_date=start_date,
            end_date=end_date,
            page_number=page_number,
            page_size=page_size,
        ))

        return [TradingResultsSpimexRequest.from_entity(x) for x in messagebus.command_result]

    except ApplicationException as e:
        logger.error(e.message)
        raise HTTPException(status_code=e.status, detail=e.message)


@router.get("/{exchange_product_id}")
async def get_product_by_exchange_product_id(
        exchange_product_id: str,
        uow: FromDishka[TradingResultUnitOfWork],
        events: FromDishka[EventHandlerMapping],
        commands: FromDishka[CommandHandlerMapping],
        page_number: int = Query(1, ge=1, description="Номер страницы"),
        page_size: int = Query(10, ge=1, le=100, description="Размер страницы"),
) -> list[TradingResultsSpimexRequest]:
    try:
        bootstrap: Bootstrap = Bootstrap(
            uow=uow, events_handlers_for_injection=events, commands_handlers_for_injection=commands
        )

        messagebus: MessageBus = await bootstrap.get_messagebus()

        await messagebus.handle(GetByExchangeProductId(
            exchange_product_id=exchange_product_id,
            page_number=page_number,
            page_size=page_size
        ))

        return [TradingResultsSpimexRequest.from_entity(x) for x in messagebus.command_result]

    except ApplicationException as e:
        logger.error(e.message)
        raise HTTPException(status_code=e.status, detail=e.message)


@router.post("parse")
async def parse_all_bulletins_from_sphinx(
        scheme: ParseAllBulletinsSpimexRequest,
        uow: FromDishka[TradingResultUnitOfWork],
        events: FromDishka[EventHandlerMapping],
        commands: FromDishka[CommandHandlerMapping],
) -> None:
    try:
        bootstrap: Bootstrap = Bootstrap(
            uow=uow, events_handlers_for_injection=events, commands_handlers_for_injection=commands
        )

        messagebus: MessageBus = await bootstrap.get_messagebus()

        await messagebus.handle(ParseAllBulletinsFromSphinx(**scheme.model_dump()))

        return messagebus.command_result

    except ApplicationException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status, detail=e.message)

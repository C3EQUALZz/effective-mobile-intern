import logging
from typing import cast

from dishka import Provider, from_context, Scope, provide, make_async_container
from faststream.kafka import KafkaBroker
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

from app.infrastructure.uow.trading_result.alchemy import SQLAlchemyTradingResultUnitOfWork
from app.infrastructure.uow.trading_result.base import TradingResultUnitOfWork
from app.logic.bootstrap import EventHandlerMapping, CommandHandlerMapping
from app.logic.commands.trading_result import ParseAllBulletinsFromSphinx
from app.logic.handlers.trading_result.commands import ParseAllBulletinsFromSphinxCommandHandler
from app.settings.config import Settings

logger = logging.getLogger(__name__)


class KafkaProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_kafka_broker(self, settings: Settings) -> KafkaBroker:
        return KafkaBroker(settings.kafka_settings.url)


class HandlerProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_mapping_command_and_command_handlers(self) -> CommandHandlerMapping:
        return cast(CommandHandlerMapping, {
            ParseAllBulletinsFromSphinx: ParseAllBulletinsFromSphinxCommandHandler
        })

    @provide(scope=Scope.APP)
    async def get_mapping_event_and_event_handlers(self) -> EventHandlerMapping:
        return cast(EventHandlerMapping, {})


class DatabaseProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_engine_client(self, settings: Settings) -> AsyncEngine:
        engine: AsyncEngine = create_async_engine(
            url=settings.database.url,
            pool_pre_ping=settings.alchemy_settings.pool_pre_ping,
            pool_recycle=settings.alchemy_settings.pool_recycle,
            echo=settings.alchemy_settings.echo,
        )

        logger.debug("Successfully connected to PostgreSQL")

        return engine

    @provide(scope=Scope.APP)
    async def get_session_maker(self, engine: AsyncEngine, settings: Settings) -> async_sessionmaker[AsyncSession]:
        session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=engine,
            autoflush=settings.alchemy_settings.auto_flush,
            expire_on_commit=settings.alchemy_settings.expire_on_commit,
        )

        return session_maker


class UoWProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_engine_client(self, session_maker: async_sessionmaker[AsyncSession]) -> TradingResultUnitOfWork:
        return SQLAlchemyTradingResultUnitOfWork(session_factory=session_maker)


container = make_async_container(
    DatabaseProvider(),
    HandlerProvider(),
    UoWProvider(),
    KafkaProvider(),
    context={
        Settings: Settings(),
    },
)

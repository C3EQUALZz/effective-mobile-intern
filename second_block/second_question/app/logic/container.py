import logging
from typing import cast

from dishka import (
    Provider,
    Scope,
    from_context,
    make_async_container,
    provide,
)
from redis.asyncio import ConnectionPool, Redis
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.infrastructure.uow.trading_result.alchemy import SQLAlchemyTradingResultUnitOfWork
from app.infrastructure.uow.trading_result.base import TradingResultUnitOfWork
from app.logic.bootstrap import (
    CommandHandlerMapping,
    EventHandlerMapping,
)
from app.logic.commands.trading_result import (
    GetByExchangeProductId,
    GetListOfTradesForSpecifiedPeriod,
    ParseAllBulletinsFromSphinx,
)
from app.logic.handlers.trading_result.commands import (
    GetByExchangeProductIdCommandHandler,
    GetListOfTradesForSpecifiedPeriodCommandHandler,
    ParseAllBulletinsFromSphinxCommandHandler,
)
from app.settings.config import Settings

logger = logging.getLogger(__name__)


class HandlerProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_mapping_command_and_command_handlers(self) -> CommandHandlerMapping:
        return cast(
            CommandHandlerMapping,
            {
                ParseAllBulletinsFromSphinx: ParseAllBulletinsFromSphinxCommandHandler,
                GetByExchangeProductId: GetByExchangeProductIdCommandHandler,
                GetListOfTradesForSpecifiedPeriod: GetListOfTradesForSpecifiedPeriodCommandHandler,
            },
        )

    @provide(scope=Scope.APP)
    async def get_mapping_event_and_event_handlers(self) -> EventHandlerMapping:
        return cast(EventHandlerMapping, {})


class RedisProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_connection_pool(self, settings: Settings) -> ConnectionPool:
        return ConnectionPool.from_url(str(settings.cache.url), encoding="utf8", decode_responses=True)

    @provide(scope=Scope.APP)
    async def get_client(self, pool: ConnectionPool) -> Redis:
        return Redis.from_pool(pool)


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
    RedisProvider(),
    UoWProvider(),
    context={
        Settings: Settings(),
    },
)

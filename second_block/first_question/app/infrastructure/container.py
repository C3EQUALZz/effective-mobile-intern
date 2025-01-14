import punq
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker
from functools import lru_cache

from app.settings.config import Settings


class ContainerConfig:
    def __init__(self) -> None:
        self.container = punq.Container()
        self.container.register(Settings, instance=Settings(), scope=punq.Scope.singleton)

    def register_database(self) -> None:
        settings: Settings = self.container.resolve(Settings)

        self.container.register(
            AsyncEngine,
            factory=lambda: create_async_engine(
                url=settings.database.url,
                pool_pre_ping=settings.alchemy_settings.pool_pre_ping,
                pool_recycle=settings.alchemy_settings.pool_recycle,
                echo=settings.alchemy_settings.echo,
            ),
            scope=punq.Scope.singleton
        )

        self.container.register(
            async_sessionmaker,
            factory=lambda: async_sessionmaker(
                bind=self.container.resolve(AsyncEngine),
                autoflush=settings.alchemy_settings.auto_flush,
                expire_on_commit=settings.alchemy_settings.expire_on_commit,
            ),
            scope=punq.Scope.singleton
        )

    def build(self) -> punq.Container:
        self.register_database()
        return self.container


@lru_cache(1)
def get_container() -> punq.Container:
    return ContainerConfig().build()

from abc import ABC
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class CommonSettings(BaseSettings, ABC):
    """
    Класс, от которого каждая настройка должна наследоваться.
    Написано с той целью, чтобы не было дублирования кода по настройке model_config.
    """

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


class DatabaseSettings(CommonSettings):
    """
    Настройки для подключения к базе данных.
    Здесь есть параметры Optional с той целью, потому что может использоваться sqlite.
    """
    host: Optional[str] = Field(alias='DATABASE_HOST', default=None)
    port: Optional[int] = Field(alias='DATABASE_PORT', default=None)
    user: Optional[str] = Field(alias='DATABASE_USER', default=None)
    password: Optional[str] = Field(alias='DATABASE_PASSWORD', default=None)
    name: str = Field(alias='DATABASE_DB')
    dialect: str = Field(alias='DATABASE_DIALECT')
    driver: str = Field(alias='DATABASE_DRIVER')

    @property
    def url(self) -> str:
        if self.dialect == 'sqlite':
            return '{}+{}:///{}'.format(
                self.dialect,
                self.driver,
                self.name
            )

        return '{}+{}://{}:{}@{}:{}/{}'.format(
            self.dialect,
            self.driver,
            self.user,
            self.password,
            self.host,
            self.port,
            self.name
        )


class SQLAlchemySettings(CommonSettings):
    """
    Настройки SQLAlchemy, полученные из env.
    """
    pool_pre_ping: bool = Field(alias="DATABASE_POOL_PRE_PING")
    pool_recycle: int = Field(alias="DATABASE_POOL_RECYCLE")
    echo: bool = Field(alias="DATABASE_ECHO")
    auto_flush: bool = Field(alias="DATABASE_AUTO_FLUSH")
    expire_on_commit: bool = Field(alias="DATABASE_EXPIRE_ON_COMMIT")


class Settings(CommonSettings):
    """
    Класс настроек, которым в дальнейшем будет оперировать приложение.
    """
    database: DatabaseSettings = DatabaseSettings()
    alchemy_settings: SQLAlchemySettings = SQLAlchemySettings()

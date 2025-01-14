import os
from abc import ABC
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class CommonSettings(BaseSettings, ABC):
    """
    Класс, от которого каждая настройка должна наследоваться.
    Написано с той целью, чтобы не было дублирования кода по настройке model_config.
    """

    model_config = SettingsConfigDict(
        env_file=os.path.expanduser("second_block/first_question/.env"),
        env_file_encoding="utf-8",
        extra="allow",
    )


class PostgresSettings(CommonSettings):
    database_name: str = Field(alias="database_name")

from abc import ABC

from app.infrastructure.utils.fetchers.base import AbstractFetcher


class Parser(ABC):
    def __init__(self, fetcher: AbstractFetcher) -> None:
        self._fetcher = fetcher

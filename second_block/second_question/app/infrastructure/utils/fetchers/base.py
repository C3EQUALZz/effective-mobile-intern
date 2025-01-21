import io
from abc import (
    ABC,
    abstractmethod,
)


class AbstractFetcher(ABC):
    """All fetchers must inherit from this class"""

    def __init__(self) -> None:
        self._headers = {"Accept": "*/*", "User-Agent": "Chrome/51.0.2704.103 Safari/537.36"}

    @abstractmethod
    async def get_page_source(self, url: str) -> str:
        """Return page content from an URL

        Args:
            url: URL

        Returns:
            page content (html, json, whatever)
        """
        ...

    @abstractmethod
    async def get_file(self, url: str) -> io.BytesIO: ...

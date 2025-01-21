import io
from typing import override

import aiohttp

from app.infrastructure.utils.fetchers.base import AbstractFetcher


class AiohttpFetcher(AbstractFetcher):
    """Fetcher, which uses aiohttp for async queries"""

    @override
    async def get_page_source(self, url: str) -> str:
        """
        Gets info from URL using aiohttp
        :param url: url for query
        :returns: info from query
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self._headers) as response:
                response.raise_for_status()
                return await response.text()

    @override
    async def get_file(self, url: str) -> io.BytesIO:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return io.BytesIO(await response.read())

import io
from collections.abc import AsyncGenerator
from datetime import (
    date,
    datetime,
)
from typing import (
    Final,
    override,
)

from playwright.async_api import async_playwright

from app.infrastructure.services.parsers.trading_result.spimex.base import AbstractSpimexParser


class SpimexAllBulletinsParser(AbstractSpimexParser):
    __URL: Final[str] = "https://spimex.com/markets/oil_products/trades/results/"

    @override
    async def parse(self, start_date: date, end_date: date) -> AsyncGenerator[tuple[date, io.BytesIO], None]:
        async for date_of_creating_file, file_url in self.__get_urls(self.__URL, start_date, end_date):
            yield date_of_creating_file, await self._fetcher.get_file(file_url)

    @staticmethod
    async def __get_urls(url: str, start_date: date, end_date: date) -> AsyncGenerator[tuple[date, str], None]:
        """Асинхронный генератор, возвращающий URL-ы для загрузки файлов."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url)

            # Принимаем условия, если нужно
            terms_container = page.locator("div.terms")
            await terms_container.locator("input[type='submit'].terms__footer__btn").click()

            next_button = page.locator("li.bx-pag-next")

            while end_date >= start_date:
                locator_to_active_page = page.locator("div.page-content__tabs__block.active")
                container = await locator_to_active_page.locator("div.accordeon-inner__item").all()

                for item in container:
                    tag_a = await item.locator("a.accordeon-inner__item-title.link.xls").first.get_attribute("href")
                    end_date = datetime.strptime(await item.locator("span").text_content(), "%d.%m.%Y").date()

                    yield end_date, "https://spimex.com" + tag_a

                # Переход на следующую страницу
                await next_button.click()

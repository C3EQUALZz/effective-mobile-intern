import io
from datetime import datetime, date
from typing import AsyncGenerator, override, Final, Tuple

from playwright.async_api import async_playwright

from infrastructure.services.parsers.trading_result.spimex.base import AbstractSpimexParser


class SpimexAllBulletinsParser(AbstractSpimexParser):
    __URL: Final[str] =  "https://spimex.com/markets/oil_products/trades/results/"

    @override
    async def parse(self, start_date: date, end_date: date) -> AsyncGenerator[Tuple[date, io.BytesIO], None]:
        async for date_of_creating_file, file_url in self.__get_urls(self.__URL, start_date, end_date):
            yield date_of_creating_file, await self._fetcher.get_file(file_url)

    @staticmethod
    async def __get_urls(url: str, start_date: date, end_date: date) -> AsyncGenerator[Tuple[date, str], None]:
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

# async def process_file(url: str):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             if response.status == 200:
#                 # Читаем файл в pandas
#                 content = await response.read()
#                 data = pd.read_excel(io.BytesIO(content), skiprows=6).iloc[:, 1:]
#                 print(data.head())
#
#                 print(f"Processed file from {url}")
#                 # Добавьте здесь нужную обработку `data`
#             else:
#                 print(f"Failed to download {url}, status: {response.status}")
#
#
# async def main(url: str, start_date: date, end_date: date):
#     queue = asyncio.Queue()
#     url_collector = asyncio.create_task(get_urls(url, start_date, end_date, queue))
#
#     async def worker():
#         while True:
#             file_url = await queue.get()
#             if file_url is None:  # Специальный маркер завершения
#                 break
#             await process_file(file_url)
#             queue.task_done()
#
#     # Запускаем несколько "воркеров" для обработки файлов
#     workers = [asyncio.create_task(worker()) for _ in range(5)]
#
#     # Ждем завершения сбора URL-ов
#     await url_collector
#
#     # Добавляем маркеры завершения в очередь
#     for _ in range(len(workers)):
#         await queue.put(None)
#
#     # Ждем завершения всех воркеров
#     await asyncio.gather(*workers)
#
#
# async def get_urls(url: str, start_date: date, end_date: date, queue: asyncio.Queue):
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=True)
#         page = await browser.new_page()
#         await page.goto(url)
#
#         terms_container = page.locator("div.terms")
#         await terms_container.locator("input[type='submit'].terms__footer__btn").click()
#
#         next_button = page.locator("li.bx-pag-next")
#
#         while end_date > start_date:
#             locator_to_active_page = page.locator("div.page-content__tabs__block.active")
#             container = await locator_to_active_page.locator("div.accordeon-inner__item").all()
#
#             for item in container:
#                 tag_a = await item.locator("a.accordeon-inner__item-title.link.xls").first.get_attribute("href")
#                 end_date = datetime.strptime(await item.locator("span").text_content(), "%d.%m.%Y").date()
#
#                 if end_date > start_date:
#                     break
#
#                 queue.put_nowait("https://spimex.com" + tag_a)
#
#             await next_button.click()
#
#         return queue
#
#
# # print(datetime.now() > datetime.strptime("01.01.2023", "%d.%m.%Y"))
# asyncio.run(
#     main("https://spimex.com/markets/oil_products/trades/results/",
#          datetime.strptime("01.01.2025", "%d.%m.%Y").date(),
#          datetime.now().date())
# )

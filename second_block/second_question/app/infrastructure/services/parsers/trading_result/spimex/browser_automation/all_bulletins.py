import asyncio
from datetime import datetime

from playwright.async_api import async_playwright


async def main(url: str, start_date: datetime, end_date: datetime):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        while end_date > start_date:
            locator_to_active_page = page.locator("div.page-content__tabs__block.active")
            container = await locator_to_active_page.locator("div.accordeon-inner__item").all()

            for item in container:
                tag_a = item.locator("a.accordeon-inner__item-title.link.xls").first
                print(tag_a)

            end_date = datetime.strptime(await item.locator("span").text_content(), "%d.%m.%Y")

        await browser.close()


print(datetime.now() < datetime.strptime("01.01.2023", "%d.%m.%Y"))
# asyncio.run(main("https://spimex.com/markets/oil_products/trades/results/", datetime.now(), datetime.strptime("01.01.2023", "%d.%m.%Y")))

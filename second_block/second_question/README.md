# Задание 2. 

## Условие

> Реальная рабочая задача - написать парсер, который скачивает бюллетень по итогам торгов с сайта [биржи](https://spimex.com/markets/oil_products/trades/results/).
> 
> Достает из бюллетени необходимые столбцы (забрать только данные из таблицы «Единица измерения: Метрическая тонна»,
> где по столбцу «Количество Договоров, шт.» значения больше 0):
> - a. Код Инструмента (exchange_product_id)
> - b. Наименование Инструмента (exchange_product_name)
> - c. Базис поставки (delivery_basis_name)
> - d. Объем Договоров в единицах измерения (volume)
> - e. Объем Договоров, руб. (total)
> - f. Количество Договоров, шт. (count)
> 
> Сохраняет полученные данные в таблицу «spimex_trading_results» со следующей структурой:
> - g. id
> - h. exchange_product_id
> - i. exchange_product_name
> - j. oil_id - exchange_product_id[:4]
> - k. delivery_basis_id - exchange_product_id[4:7]
> - l. delivery_basis_name
> - m. delivery_type_id - exchange_product_id[-1]
> - n. volume
> - o. total
> - p. count
> - q. date
> - r. created_on
> - s. updated_on
> 
> Необходимо создать базу данных, которая будет хранить информацию по итогам торгов начиная с 2023 года.

## Что использовалось? 

- [playwright](https://playwright.dev/)
- [fastapi](https://playwright.dev/)
- [dishka](https://dishka.readthedocs.io/en/stable/)
- [pandas](https://pandas.pydata.org/)
- [aiohttp](https://docs.aiohttp.org/en/stable/)

Для парсинга использовал библиотеку playwright, которая умеет асинхронно работать с веб браузером. 
В задаче использовался динамический сайт, где используется пагинация, поэтому выбрана была такая библиотека.

В дальнейших задачах требуется написать API, который будет возвращать данные с базы данных, поэтому автор решил сразу написать.

## Какая архитектура? 

Здесь используется подход DDD + CQRS, более подробно объяснение моей архитектуры можете найти [здесь](https://github.com/C3EQUALZz/library-console-app).






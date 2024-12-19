import asyncio
import json

import aiohttp
from lxml import etree

# Заголовки для запросов
headers = {
    "Accept": "*/*",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Referer": "https://yandex.ru/maps/org/tsentrofinans/1394464199/?ll=39.252326%2C51.670786&z=16",
    "Cookie": (
        "i=CNHdLYo+nqnj+rDuKQcyUuDKraqK5X/feOtFb5WNmr7g2tW9HNsoToeL98B7e9R8tCEUFJx1f7+c8l6bWSAY+FSyT3E=;"
        " yandexuid=7853401791734514505; yuidss=7853401791734514505; ymex=2049874505.yrts.1734514505#2049874505.yrtsi.1734514505;"
        " yashr=6299392811734514704; receive-cookie-deprecation=1; gdpr=0;"
        "_ym_isad=2; _ym_uid=1733748629829214352; _ym_d=1734514920;"
        " yabs-vdrf=A0; is_gdpr=0; is_gdpr_b=CPeCThDkpAI=;"
        " yandex_expboxes=1173376%2C0%2C15%3B1175497%2C0%2C60%3B1002325%2C0%2C7%3B1176583%2C0%2C63;"
        "1169584%2C0%2C45%3B1178183%2C0%2C31%3B1168657%2C0%2C48;"
        "1176523%2C0%2C0%3B1068828%2C0%2C15%3B1131450%2C0%2C96;"
        "998603%2C0%2C17%3B663872%2C0%2C62;663859%2C0%2C67;"
        "1168450%2C0%2C16%3B1170166%2C0%2C11%3B1170594%2C0%2C80;"
        " spravka=dD0xNzAyOTg5MDA1O2k9MTkzLjEwNi40Mi4xODA7RD05NDg1QzZCRTE5OUY3MkY0RjUwREJEMUE1N0ZFMUI2MEJBMEQ5RkRCMjgzNzBDOENDQTc4MTMyQ0MwMjhFNzBDQUE3MTZFQTQ2MTYzREJBRTt1PTE3MDI5ODkwMDU0NjM3MDY2NTE7aD1lZTVlNmI5NGEzNzFhNmZhY2MzNzUwZDc1Y2U3YWJkMQ==;"
        "_yasc=gEo80kvWd5o5CM9zZUDm/1L8tNM85E9cXfz9sO8S5jw806y8Xw8qo/SNjqafA5cdT+nyiiQNJss=;"
        "_ym_visorc=b; maps_session_id=1734526224644884-11266174183736591989-balancer-l7leveler-kubr-yp-klg-313-BAL;"
        " bh=EkEiR29vZ2xlIENocm9tZSI7dj0iMTMxIiwgIkNocm9taXVtIjt2PSIxMzEiLCAiTm90X0EgQnJhbmQiO3Y9IjI"
        "IhoFIng4NiIiECIxMzEuMC42Nzc4LjEwOCIqAj8wMgIiIjoHIkxpbnV4IkIJIjYuMS4xMTkiSgQiNjQiUl"
        "lR29vZ2xlIENocm9tZSI7dj0iMTMxLjAuNjc3OC4xMDgiLCAiQ"
        "mhyb21pdW0iO3Y9IjEzMS4wLjY3NzguMTA4IiwgIk5vdF9BIEJyYW5kIjt"
        "]"
    ),
}


# Чтение данных из JSON файла
async def load_data():
    with open("company_links.json", "r", encoding="utf-8") as file:
        return json.load(file)


# Асинхронная функция для выполнения запросов
async def fetch(session, url):
    try:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()  # Проверка на ошибки HTTP
            return await response.text()
    except aiohttp.ClientError as e:
        print(f"Ошибка при запросе")
        return None


# Парсинг данных из ответа
def parse_data(response):
    tree = etree.fromstring(response, etree.HTMLParser())

    check_mark = tree.xpath("//h1/span/@class")
    if check_mark == ["business-verified-badge _prioritized"]:
        return None  # Пропускаем проверенные компании

    company_name = tree.xpath("//h1[@class='orgpage-header-view__header']/text()")
    company_number = tree.xpath(
        '//div[@class="orgpage-phones-view__phone-number"]/text()'
    )
    print(company_name)

    if company_name and company_number:
        return {
            "company_name": company_name[0].strip(),
            "company_number": company_number[0].strip(),
        }
    return None


# Основная асинхронная функция для сбора данных
async def gather_data(data):
    collected_data = {}

    async with aiohttp.ClientSession() as session:
        for city, links in data.items():
            collected_data[city] = []  # Создаем список для каждой категории

            tasks = [fetch(session, link) for link in links]  # Ограничиваем до 5 ссылок
            responses = await asyncio.gather(*tasks)

            for response in responses:
                if response is not None:
                    parsed_data = parse_data(response)
                    if parsed_data:
                        collected_data[city].append(parsed_data)

    return collected_data


# Сохранение собранных данных в новый JSON файл
def save_data(collected_data):
    with open("company_numbers.json", "w", encoding="utf-8") as outfile:
        json.dump(collected_data, outfile, indent=4, ensure_ascii=False)


# Запуск основной программы
async def main():
    data = await load_data()
    collected_data = await gather_data(data)

    if collected_data:
        save_data(collected_data)
        print("Сбор данных завершен!")
    else:
        print("Нет собранных данных для сохранения.")


if __name__ == "__main__":
    asyncio.run(main())

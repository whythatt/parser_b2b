import json
import time

import requests
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,nl;q=0.6",
    "Connection": "keep-alive",
    "Cookie": "i=XPCSirj7WbU6OiiuP5Fgj2Bq6Sehuk35p4ZQvs2cGqZOsYPYryYDbRDrKC+uj/PQ9TdeI+vKJG6LWWews1aYe9jF95A=; yandexuid=5114213771733735474; yashr=3154611681733735474; yuidss=5114213771733735474; ymex=2049095479.yrts.1733735479; receive-cookie-deprecation=1; is_gdpr=0; is_gdpr_b=CNGecBCMowI=; amcuid=5968322501733735928; gdpr=0; _ym_uid=1733748629829214352; _ym_d=1733748633; yandex_expboxes=1167773%2C0%2C4%3B1068828%2C0%2C89%3B1131450%2C0%2C78%3B998603%2C0%2C25%3B663874%2C0%2C9%3B663859%2C0%2C19%3B1168450%2C0%2C45%3B1170165%2C0%2C59%3B1172168%2C0%2C20%3B1163920%2C0%2C53%3B1170594%2C0%2C27; _ym_isad=2; yclid_src=yandex.ru/maps/org/196518596709:10431374298906361855:5114213771733735474; yabs-dsp=mts_banner.R3I4ejEwbXpRSTZBbGRMUE9wZXZUZw==; _yasc=U4KOdMMRqthm0ET+pm75c2EwXhoisNx4SeI2/ePcekoWJ4Fyaz6BEaqLADRoGkQoiuQJlJswVEWH; yabs-vdrf=A0; maps_session_id=1733924934667124-1342109850547945316-balancer-l7leveler-kubr-yp-klg-249-BAL; yp=1734529796.szm.1:1366x768:1366x637; k50uuid=ddc78aa7-0638-47a4-ae95-2a2355b175b5; k50lastvisit=db546baba3acb079f91946f80b9078ffa565e36d.945b27d7c97f40d2a056f2a59d3b474296ea10e8.db546baba3acb079f91946f80b9078ffa565e36d.e69f3efe883d7cc40ffc0de9a44cff925db77d90.1733924997829; k50sid=9969e6a4-2157-4a7a-a579-35765410c8b4; _ym_visorc=b; bh=EkEiR29vZ2xlIENocm9tZSI7dj0iMTMxIiwgIkNocm9taXVtIjt2PSIxMzEiLCAiTm90X0EgQnJhbmQiO3Y9IjI0IhoFIng4NiIiECIxMzEuMC42Nzc4LjEwOCIqAj8wMgIiIjoHIkxpbnV4IkIJIjYuMS4xMTkiSgQiNjQiUl0iR29vZ2xlIENocm9tZSI7dj0iMTMxLjAuNjc3OC4xMDgiLCAiQ2hyb21pdW0iO3Y9IjEzMS4wLjY3NzguMTA4IiwgIk5vdF9BIEJyYW5kIjt2PSIyNC4wLjAuMCJaAj8wYIux5roGahncyumIDvKst6UL+/rw5w3r//32D6SYzYcI",
    "Host": "api-maps.yandex.ru",
    "Origin": "https://yandex.ru",
    "X-Requested-With": "XMLHttpRequest",
}

# Чтение данных из JSON файла
with open("company_links.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Словарь для хранения собранных данных
collected_data = {}

# Проход по каждой ссылке в JSON
for city, links in data.items():
    collected_data[city] = []  # Создаем список для каждого города

    for link in links:
        try:
            response = requests.get(link, headers=headers)
            response.raise_for_status()  # Проверка на ошибки HTTP

            # Парсинг HTML страницы
            tree = etree.fromstring(response.content, etree.HTMLParser())

            # Здесь вы можете определить, какие данные вам нужны. Например:
            check_mark = tree.xpath(
                '//span[@class="business-verified-badge _prioritized"]/@class'
            )
            print(check_mark)
            if check_mark != None:
                if check_mark[0] == "business-verified-badge _prioritized":
                    continue

            company_name = tree.xpath(
                "//h1[@class='orgpage-header-view__header']/text()"
            )

            company_number = tree.xpath(
                '//div[@class="orgpage-phones-view__phone-number"]/text()'
            )
            print(check_mark, company_name)

            if company_number:
                # print(f"{company_name[0]} || {company_number[0]}")

                # Сохраняем данные в словарь
                collected_data[city].append(
                    {
                        "company_name": company_name[0],
                        "company_number": company_number[0],
                    }
                )

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к {link}: {e}")

# Сохранение собранных данных в новый JSON файл
with open("company_numbers.json", "w", encoding="utf-8") as outfile:
    json.dump(collected_data, outfile, indent=4, ensure_ascii=False)

print("Сбор данных завершен!")

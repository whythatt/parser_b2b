import json
import time

import requests
from lxml import etree

# Заголовки для запросов
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Cookie": "maps_los=0; i=CNHdLYo+nqnj+rDuKQcyUuDKraqK5X/feOtFb5WNmr7g2tW9HNsoToeL98B7e9R8tCEUFJx1f7+c8l6bWSAY+FSyT3E=; yandexuid=7853401791734514505; yuidss=7853401791734514505; ymex=2049874505.yrts.1734514505#2049874505.yrtsi.1734514505; yashr=6299392811734514704; receive-cookie-deprecation=1; gdpr=0; _ym_isad=2; _ym_uid=1733748629829214352; _ym_d=1734514920; yabs-vdrf=A0; is_gdpr=0; is_gdpr_b=CPeCThDkpAI=; yandex_expboxes=1173376%2C0%2C15%3B1175497%2C0%2C60%3B1002325%2C0%2C7%3B1176583%2C0%2C63%3B1169584%2C0%2C45%3B1178183%2C0%2C31%3B1168657%2C0%2C48%3B1176523%2C0%2C0%3B1068828%2C0%2C15%3B1131450%2C0%2C96%3B998603%2C0%2C17%3B663872%2C0%2C62%3B663859%2C0%2C67%3B1168450%2C0%2C16%3B1170166%2C0%2C11%3B1170594%2C0%2C80; _ym_visorc=b; _yasc=aW0oab0FB3ffAqr7AKmK+/WFZCxTWqBEdFotbrzO1IW6pZS3qWRVYgGUERBtSlaOrDiNaHXx4OcUL/vX; spravka=dD0xNzM0NTI4NDQxO2k9MTkzLjEwNi40Mi4xODA7RD04MjhFRkZBNUNFNzhDREZEQjA1ODJFMUYwN0QyMDZGMzNBQUY0QzczNTU2NjAwNUY5N0IxODYzQ0Q1NzUyNzg5RTVBMkI2QzlGOEE4NDYzQkRBNzA2MjIyQTBDQTdBQzNGMDEyRTM5MUIyRUIxNTQ2RkQ0OTk4MzFDMkE1RjFCOUQzQ0M3RDI2NTJDMERGNEE0RTt1PTE3MzQ1Mjg0NDEzNjg2MzQyMDA7aD04ZDI5YmI1ZGVjOWZmNDJlNmMzYmEwOTZkZDhiYWY0OQ==; maps_session_id=1734528441406694-10720261644166654983-balancer-l7leveler-kubr-yp-klg-313-BAL; bh=EkEiR29vZ2xlIENocm9tZSI7dj0iMTMxIiwgIkNocm9taXVtIjt2PSIxMzEiLCAiTm90X0EgQnJhbmQiO3Y9IjI",
}

# Чтение данных из JSON файла
with open("company_links.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Словарь для хранения собранных данных
collected_data = {}

# Проход по каждой ссылке в JSON
for city, links in data.items():
    collected_data[city] = []  # Создаем список для каждого города

    for link in links[:5]:
        try:
            # Случайный выбор User-Agent из списка
            response = requests.get(link, headers=headers)
            response.raise_for_status()  # Проверка на ошибки HTTP

            # Парсинг HTML страницы
            tree = etree.fromstring(response.content, etree.HTMLParser())

            # Проверка на наличие специального знака проверки
            check_mark = tree.xpath("//h1/span/@class")
            if check_mark == ["business-verified-badge _prioritized"]:
                continue

            company_name = tree.xpath(
                "//h1[@class='orgpage-header-view__header']/text()"
            )
            if company_name:
                company_name = company_name[0].strip()

            company_number = tree.xpath(
                '//div[@class="orgpage-phones-view__phone-number"]/text()'
            )
            if company_number:
                company_number = company_number[0].strip()

            if company_number:
                # Сохраняем данные в словарь
                collected_data[city].append(
                    {
                        "company_name": company_name,
                        "company_number": company_number,
                    }
                )

            captcha_check = tree.xpath("//h1/text()")
            if captcha_check and "капча" in captcha_check[0].lower():
                print("Капча обнаружена!")
                # Здесь можно добавить логику для решения капчи

            else:
                print(company_name, "+", company_number)

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе: {e}")

# Сохранение собранных данных в новый JSON файл
with open("company_numbers.json", "w", encoding="utf-8") as outfile:
    json.dump(collected_data, outfile, indent=4, ensure_ascii=False)

print("Сбор данных завершен!")

import json
import time

from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Настройка Selenium WebDriver
driver = webdriver.Firefox()

# Чтение данных из JSON файла
with open("company_links.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Словарь для хранения собранных данных
collected_data = {}

# Проход по каждой ссылке в JSON
for city, links in data.items():
    collected_data[city] = []  # Создаем список для каждого города

    for link in links:  # Ограничиваем количество ссылок для обработки
        try:
            driver.get(link)  # Переход к ссылке
            time.sleep(2)  # Задержка для загрузки страницы

            # Получаем HTML-код страницы
            page_source = driver.page_source
            tree = etree.fromstring(page_source, etree.HTMLParser())

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

        except Exception as e:
            print(f"Ошибка при обработке {link}: {e}")

# Закрытие драйвера после завершения работы
driver.quit()

# Сохранение собранных данных в новый JSON файл
with open("company_numbers.json", "w", encoding="utf-8") as outfile:
    json.dump(collected_data, outfile, indent=4, ensure_ascii=False)

print("Сбор данных завершен!")

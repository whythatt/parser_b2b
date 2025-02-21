import json
import time

from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Настройка Selenium WebDriver
driver = webdriver.Chrome()

# Чтение данных из JSON файла
with open("company_links_more.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Словарь для хранения собранных данных
collected_data = {}

start_time = time.time()

# Проход по каждой ссылке в JSON
for city, links in data.items():
    collected_data[city] = []  # Создаем список для каждого города

    for link in links:  # Ограничиваем количество ссылок для обработки
        try:
            driver.get(link)  # Переход к ссылке
            # Ожидание загрузки страницы
            time.sleep(0.1)
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )

            # Получаем HTML-код страницы
            page_source = driver.page_source
            tree = etree.fromstring(page_source, etree.HTMLParser())

            # # Проверка на наличие специального знака проверки
            # check_mark = tree.xpath("//h1/span/@class")
            # if check_mark == ["business-verified-badge _prioritized"]:
            #     continue
            #
            # company_name = tree.xpath(
            #     "//h1[@class='orgpage-header-view__header']/text()"
            # )
            # if company_name:
            #     company_name = company_name[0].strip()
            #
            # category = tree.xpath(
            #     "//a[@class='breadcrumbs-view__breadcrumb _outline'][3]/text()"
            # )
            # if category:
            #     category = category[0].strip()
            #
            # company_number = tree.xpath(
            #     '//div[@class="orgpage-phones-view__phone-number"]/text()'
            # )
            # if company_number:
            #     company_number = company_number[0].strip()
            #
            # link = tree.xpath('//a[@class="business-urls-view__link"]/@href')
            # if link:
            #     link = link[0].strip()
            #
            # if company_number:
            #     # Сохраняем данные в словарь
            #     collected_data[city].append(
            #         {
            #             "company_name": company_name,
            #             "company_number": company_number,
            #             "category": category,
            #             "website": link,
            #         }
            #     )
            #
            # captcha_check = tree.xpath("//h1/text()")
            # if captcha_check and "капча" in captcha_check[0].lower():
            #     print("Капча обнаружена!")
            #     # Здесь можно добавить логику для решения капчи

            # else:
            #     print(company_name)

            company_name = tree.xpath(
                "//h1[@class='orgpage-header-view__header']/text()"
            )
            if company_name:
                company_name = company_name[0].strip()

            website = tree.xpath('//a[@class="business-urls-view__link"]/@href')
            if website:
                website = website[0].strip()

            address = tree.xpath(
                '//div[@class="business-contacts-view__address-link"]/[1]/text()'
            )
            if address:
                address = address[0].strip()

            if website:
                # Сохраняем данные в словарь
                collected_data[city].append(
                    {
                        "company_name": company_name,
                        "address": address,
                        "website": website,
                    }
                )

        except Exception:
            print(f"Ошибка при обработке {link}")

# Закрытие драйвера после завершения работы
driver.quit()

# Сохранение собранных данных в новый JSON файл
with open("company_numbers.json", "w", encoding="utf-8") as outfile:
    json.dump(collected_data, outfile, indent=4, ensure_ascii=False)

end_time = time.time()

print(f"Сбор данных завершен! время: {(end_time - start_time) / 60:.2f}")

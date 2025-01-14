import json
import time
from concurrent.futures import ThreadPoolExecutor

from fake_useragent import UserAgent
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth


# Настройка Selenium WebDriver
def create_driver():
    # ua = UserAgent()
    options = webdriver.ChromeOptions()
    # options.add_argument(f'--user-agent={ua.random}')
    # options.add_argument("--headless")  # Режим без окна
    driver = webdriver.Chrome(options=options)

    return driver


# Чтение данных из JSON файла
with open("company_links.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Словарь для хранения собранных данных
collected_data = {}


def process_link(link):
    try:
        driver = create_driver()  # Создаем новый WebDriver для каждого потока

        driver.get(link)

        # Ожидание загрузки страницы
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )

        # Получаем HTML-код страницы
        page_source = driver.page_source
        tree = etree.fromstring(page_source, etree.HTMLParser())

        # Проверка на наличие специального знака проверки
        check_mark = tree.xpath("//h1/span/@class")
        if check_mark == ["business-verified-badge _prioritized"]:
            result = None
        else:
            company_name = tree.xpath(
                "//h1[@class='orgpage-header-view__header']/text()"
            )
            if company_name:
                company_name = company_name[0].strip()

            category = tree.xpath(
                "//a[@class='breadcrumbs-view__breadcrumb _outline'][3]/text()"
            )
            if category:
                category = category[0].strip()

            company_number = tree.xpath(
                '//div[@class="orgpage-phones-view__phone-number"]/text()'
            )
            if company_number:
                company_number = company_number[0].strip()

            link = tree.xpath('//a[@class="business-urls-view__link"]/@href')
            if link:
                link = link[0].strip()

            print(company_name)

            if company_number:
                result = {
                    "company_name": company_name,
                    "company_number": company_number,
                    "category": category,
                    "website": link,
                }
            else:
                result = None

        driver.quit()  # Закрываем WebDriver после использования

        return result

    except Exception as e:
        print(f"Ошибка при обработке {link}: {e}")
        return None


def main():
    global collected_data
    tasks = []

    # Выбираем 3 города для параллельной обработки
    cities = list(data.keys())[:3]

    for city in cities:
        tasks.extend(data[city])

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(process_link, tasks))

    index = 0
    for city in cities:
        collected_data[city] = [
            result
            for link, result in zip(
                data[city], results[index : index + len(data[city])]
            )
            if result
        ]
        index += len(data[city])

    # Сохранение собранных данных в новый JSON файл
    with open("company_numbers.json", "w", encoding="utf-8") as outfile:
        json.dump(collected_data, outfile, indent=4, ensure_ascii=False)

    end_time = time.time()

    print(f"Сбор данных завершен! время: {(end_time - start_time) / 60:.2f}")


if __name__ == "__main__":
    main()

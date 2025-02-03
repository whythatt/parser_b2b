import json
import time
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# Настройка Selenium WebDriver
def create_driver():
    # ua = UserAgent()
    options = webdriver.ChromeOptions()
    # options.add_argument(f"--user-agent={ua.random}")
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    return driver


# Чтение данных из JSON файла
with open("company_links.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Словарь для хранения собранных данных
collected_data = {}

# Создаем один WebDriver для всех запросов
driver = create_driver()

# Очередь для синхронизации доступа к WebDriver
driver_queue = Queue()
driver_queue.put(driver)


def process_link(link):
    try:
        # Получаем WebDriver из очереди
        driver = driver_queue.get()

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

        # Возвращаем WebDriver в очередь
        driver_queue.put(driver)

        return result

    except Exception:
        print(f"Ошибка при обработке {link}")
        driver_queue.put(driver)
        return None


# def process_link(link):
#     try:
#         # Получаем WebDriver из очереди
#         driver = driver_queue.get()
#
#         driver.get(link)
#
#         # Ожидание загрузки страницы
#         WebDriverWait(driver, 5).until(
#             EC.presence_of_element_located((By.TAG_NAME, "h1"))
#         )
#
#         # Получаем HTML-код страницы
#         page_source = driver.page_source
#         tree = etree.fromstring(page_source, etree.HTMLParser())
#
#         # Проверка на наличие специального знака проверки
#         check_mark = tree.xpath("//h1/span/@class")
#         if check_mark == ["business-verified-badge _prioritized"]:
#             return None
#
#         company_name = tree.xpath("//h1[@class='orgpage-header-view__header']/text()")
#         category = tree.xpath(
#             "//a[@class='breadcrumbs-view__breadcrumb _outline'][3]/text()"
#         )
#         company_number = tree.xpath(
#             '//div[@class="orgpage-phones-view__phone-number"]/text()'
#         )
#         link = tree.xpath('//a[@class="business-urls-view__link"]/@href')
#
#         print(company_name[0])
#
#         result = {
#             "company_name": company_name[0].strip() if company_name else None,
#             "category": category[0].strip() if category else None,
#             "company_number": company_number[0].strip() if company_number else None,
#             "website": link[0].strip() if link else None,
#         }
#
#         # Возвращаем WebDriver в очередь
#         driver_queue.put(driver)
#
#         return result
#
#     except Exception as e:
#         print(f"Ошибка при обработке {link}: {e}")
#         # Возвращаем WebDriver обратно в очередь даже в случае ошибки
#         driver_queue.put(driver)
#         return None


def main():
    global collected_data
    tasks = [link for links in data.values() for link in links]

    start_time = time.time()

    # Используем max_workers=1, чтобы задержка работала как ожидается
    with ThreadPoolExecutor(max_workers=1) as executor:
        results = list(executor.map(process_link, tasks))

    index = 0
    for city, links in data.items():
        collected_data[city] = [
            result
            for link, result in zip(links, results[index : index + len(links)])
            if result
        ]
        index += len(links)

    # Закрытие драйвера после завершения работы
    driver.quit()

    # Сохранение собранных данных в новый JSON файл
    with open("company_numbers.json", "w", encoding="utf-8") as outfile:
        json.dump(collected_data, outfile, indent=4, ensure_ascii=False)

    end_time = time.time()

    print(f"Сбор данных завершен! время: {(end_time - start_time) / 60:.2f}")


if __name__ == "__main__":
    main()

import json
import time
from concurrent.futures import ThreadPoolExecutor

from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# Настройка драйвера
def create_driver():
    driver = webdriver.Chrome()
    return driver


# Список городов и категорий
citys = [
    "Казань",
    "Краснодар",
    "Курск",
]
categories = [
    "батутный центр",
    "дизайн интерьеров",
]

# Словарь для хранения собранных ссылок
all_com_links_dict = {}


def process_city(city):
    try:
        driver = create_driver()
        driver.get("https://yandex.ru/maps")
        time.sleep(10)

        all_city_links = []

        for category in categories:
            time.sleep(3)
            # Поиск по запросу
            search_box = driver.find_element(By.CSS_SELECTOR, ".input__control")
            search_box.clear()  # Очистка поля перед вводом
            search_box.send_keys(f"{city} {category}")
            search_box.send_keys(Keys.RETURN)

            # Прокрутка страницы до загрузки всех данных (можно адаптировать под ваши нужды)
            print(category)
            time.sleep(5)
            checker = driver.find_elements(By.CSS_SELECTOR, ".add-business-view")
            if not checker:
                WebDriverWait(driver, 100).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, ".scroll__container")
                    )
                )

                # Прокрутка указанного блока до загрузки всех данных
                last_height = driver.execute_script(
                    "return document.querySelector('.scroll__container').scrollHeight"
                )
                time.sleep(3)

                while True:
                    elem = driver.find_element(By.CLASS_NAME, "scroll__container")
                    elem.send_keys(Keys.END)
                    time.sleep(7)
                    new_height = driver.execute_script(
                        "return document.querySelector('.scroll__container').scrollHeight"
                    )
                    if new_height == last_height:
                        break

                    last_height = new_height

            page_source = driver.page_source
            tree = etree.fromstring(page_source, etree.HTMLParser())

            all_links = tree.xpath('//a[@class="link-overlay"]/@href')

            for link in all_links:
                all_city_links.append("https://yandex.ru" + link)

        # Добавляем ссылки в общий список
        all_com_links_dict[city] = all_city_links

        driver.quit()  # Закрываем WebDriver после использования

    except Exception:
        print(f"Ошибка при обработке {city}")


def main():
    global all_com_links_dict

    # Выбираем первые 3 города для параллельной обработки
    cities_to_process = citys[:3]

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(process_city, cities_to_process)

    # Сохранение всех собранных данных в JSON файл
    with open("company_links.json", "w", encoding="utf-8") as file:
        json.dump(all_com_links_dict, file, indent=4, ensure_ascii=False)

    end_time = time.time()

    print(f"Сбор данных завершен! время: {(end_time - start_time) / 60:.2f}")


if __name__ == "__main__":
    main()

import json
import threading
import time

from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Списки городов и категорий
citys = ["Липецк", "воронеж", "тула"]
categories = [
    "ветеринарные клиники",
    "гостиницы",
    "дизайн интерьеров",
    "зоомагазины",
    "интернет-магазины",
    "кальян-бары",
]  # Добавьте все 43 категории сюда

# Настройка драйвера
options = Options()
# options.headless = True  # Если нужно запускать в headless режиме


# Функция для парсинга данных в одном окне
def parse_data(city, driver):
    all_city_links = []
    for category in categories:
        time.sleep(1)
        # Поиск по запросу
        search_box = driver.find_element(By.CSS_SELECTOR, ".input__control")

        # Очистка поля
        actions = ActionChains(driver)
        actions.click(search_box)
        actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL)
        actions.send_keys(Keys.BACKSPACE)
        actions.perform()

        # Установка курсора в начало и ввод нового текста
        search_box.send_keys(Keys.HOME)
        search_box.send_keys(f"{city} {category}")
        time.sleep(1)  # Небольшая пауза перед отправкой
        search_box.send_keys(Keys.RETURN)

        # Прокрутка страницы до загрузки всех данных (можно адаптировать под ваши нужды)
        time.sleep(5)
        checker = driver.find_elements(By.CSS_SELECTOR, ".add-business-view")
        if not checker:
            WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".scroll__container"))
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

    return all_city_links


# Создание окон для каждого города
def create_driver():
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )


# Основная функция
def main():
    all_com_links_dict = {}
    drivers = [create_driver() for _ in range(len(citys))]

    def parse_city(city, driver):
        driver.get("https://yandex.ru/maps")
        all_city_links = parse_data(city, driver)
        all_com_links_dict[city] = all_city_links
        driver.quit()

    threads = []
    for i, city in enumerate(citys):
        thread = threading.Thread(target=parse_city, args=(city, drivers[i]))
        print(drivers[i])
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    # Сохранение всех собранных данных в JSON файл
    with open("company_links.json", "w", encoding="utf-8") as file:
        json.dump(all_com_links_dict, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()

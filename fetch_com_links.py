import json
import time

import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Список городов
citys = [
    "Казань",
    "Краснодар",
    "Курск",
    "Липецк",
    # "Воронеж",
    # "Екатеринбург",
    # "Калининград",
    # "Москва",
    # "Пермь",
    # "Ростов-на-Дону",  # Полное название
    # "Омск",
    # "Орел",
    # "Абакан",
    # "Архангельск",
    # "Астрахань",
    # "Барнаул",
    # "Белгород",
    # "Бийск",
    # "Благовещенск",
    # "Братск",
    # "Брянск",
    # "Великий Новгород",
    # "Владивосток",
    # "Владикавказ",
    # "Владимир",
    # "Волгоград",
    # "Вологда",
    # "Грозный",
    # "Иваново",
    # "Ижевск",
    # "Иркутск",
    # "Калуга",
    # "Каменск-Уральский",
    # "Кемерово",
    # "Киров",
    # "Комсомольск-на-Амуре",
    # "Королев",
    # "Кострома",
    # "Красноярск",
    # "Магнитогорск",
    # "Махачкала",
    # "Мурманск",
    # "Набережные Челны",  # Полное название
    # "Нижний Новгород",  # Полное название
    # "Новокузнецк",
    # "Новороссийск",
    # "Новосибирск",  # Исправлено с 'Ново ибирск'
    # "Норильск",
    # "Оренбург",
    # "Пенза",
    # "Первоуральск",
    # "Прокопьевск",
    # "Псков",
    # "Рыбинск",
    # "Рязань",  # Исправлено с 'Cамара' на 'Самара'
    # "Самара",  # Исправлено
    # "Санкт-Петербург",  # Полное название
    # "Саратов",
    # "Севастополь",  # Полное название
    # "Северодвинск",
    # "Симферополь",
    # "Сочи",
    # "Ставрополь",
    # "Тамбов",
    # "Тверь",
    # "Тольяти",
    # "Томск",
    # "Тула",
    # "Tюмень",
    # "Улан-Удэ",
    # "Ульяновск",
    # "Уфа",
    # "Хабаровск",
    # "Чебоксары",
    # "Челябинск",
    # "Шахты",
    # "Энгельс",
    # "Южно-Сахалинск",
    # "Якутск",
    # "Ярославль",
]
categories = [
    # "микрозайм",
    # "туристические агентства",
    # "магазин одежды",
    # "кафе",
    # "рестораны",
    # "автосервисы",
    # "фитнес-клубы",
    # "магазины электроники",
    # "магазины товаров для дома",
    # "парикмахерские",
    # "строительные магазины",
    # "клининговые услуги",
    # "коворкинги",
    # "рыбалка",
    # "вязание",
    # "охота",
    # "гостиницы",
    # "аренда помещений",
    # "автошколы",
    # "развлечения",
    # "батутный центр",
    "вейп шопы",
    "Салон красоты",
]

# Настройка драйвера
# options = webdriver.ChromeOptions()
# options.add_argument("--disable-dev-shm-usage")
# driver = webdriver.Chrome(options=options)
driver = webdriver.Firefox()

all_company_links = {}

driver.get("https://yandex.ru/maps")

for city in citys:
    for category in categories:
        print(category)
        time.sleep(3)
        # Открытие Яндекс Карт

        # Поиск по запросу
        search_box = driver.find_element(By.CSS_SELECTOR, ".input__control")
        search_box.clear()  # Очистка поля перед вводом
        search_box.send_keys(f"{city} {category}")
        search_box.send_keys(Keys.RETURN)

        # Прокрутка страницы до загрузки всех данных (можно адаптировать под ваши нужды)
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".scroll__container"))
        )

        # Прокрутка указанного блока до загрузки всех данных
        last_height = driver.execute_script(
            "return document.querySelector('.scroll__container').scrollHeight"
        )
        time.sleep(3)

        count = 0
        while True:
            elem = driver.find_element(By.CLASS_NAME, "scroll__container")
            elem.send_keys(Keys.END)
            time.sleep(8)
            new_height = driver.execute_script(
                "return document.querySelector('.scroll__container').scrollHeight"
            )
            count += 1
            print(count)
            if new_height == last_height:
                break

            last_height = new_height

        page_source = driver.page_source
        tree = etree.fromstring(page_source, etree.HTMLParser())

        all_links = tree.xpath('//a[@class="link-overlay"]/@href')

        company_links = ["https://yandex.ru" + link for link in all_links]

        # Добавляем ссылки в словарь под названием города
        all_company_links[category] = company_links
        with open("company_links.json", "a", encoding="utf-8") as file:
            json.dump(
                {f"{category}": company_links}, file, indent=4, ensure_ascii=False
            )

# Сохранение всех собранных данных в JSON файл
# with open("company_links.json", "w", encoding="utf-8") as file:
#     json.dump(all_company_links, file, indent=4, ensure_ascii=False)

# Закрытие драйвера
driver.quit()

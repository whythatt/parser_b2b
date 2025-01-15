import json
import time

from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Список городов
citys = [
    "Курск",
    # "Казань",
    # "Краснодар",
    # "Липецк",
    # "Екатеринбург",
    # "Пенза",
    # "Москва",
    # "Пермь",
    # "Ростов-на-Дону",  # Полное название
    # "Абакан",
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
    # "Новокузнецк",
    # "Новороссийск",
    # "Новосибирск",  # Исправлено с 'Ново ибирск'
    # "Норильск",
    # "Оренбург",
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
    "графический дизайн",
    "автосервисы",
    "агентства недвижимости",
    "бары и пабы",
    "батутный центр",
    "вязание",
    "ветеринарные клиники",
    "гостиницы",
    "дизайн интерьеров",
    "зоомагазины",
    "интернет-магазины",
    "кальян-бары",
    "кафе",
    "квесты",
    "клининговые услуги",
    "кофейни",
    "магазин одежды",
    "магазины электроники",
    "магазины товаров для дома",
    "мебельные магазины",
    "охота",
    "парикмахерские",
    "парфюмерия и косметика",
    "переводчики",
    "печать на футболках",
    "пирсинг-салоны",
    "праздничные агентства",
    "продажа и ремонт бытовой техники",
    "развлечения",
    "рестораны",
    "рыбалка",
    "салон красоты",
    "свадебные салоны",
    "секонд хенд",
    "спортивные магазины",
    "строительные магазины",
    "туристические агентства",
    "туристические базы",
    "фитнес-клубы",
    "флористические услуги",
    "фотостудии",
    "химчистки",
    "бассейны",
]

# Настройка драйвера
driver = webdriver.Firefox()

all_com_links_dict = {}

driver.get("https://yandex.ru/maps")

for city in citys:
    all_city_links = []
    for category in categories:
        time.sleep(3)
        # Открытие Яндекс Карт

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

        # Добавляем ссылки в общий список
    all_com_links_dict[city] = all_city_links

# Сохранение всех собранных данных в JSON файл
with open("company_links.json", "w", encoding="utf-8") as file:
    json.dump(all_com_links_dict, file, indent=4, ensure_ascii=False)

# Закрытие драйвера
driver.quit()
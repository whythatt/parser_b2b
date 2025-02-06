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
    "Рязань",
    # "Казань",
    # "Краснодар",
    # "Екатеринбург",
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
    # "Самара",  # Исправлено
    # "Санкт-Петербург",  # Полное название
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
]
categories = [
    "Салон красоты",
    "Гостиница",
    "Автосервис, автотехцентр",
    "Стоматологическая клиника",
    "Ресторан",
    "Магазин цветов",
    "Медцентр, клиника",
    "Кафе",
    "Ногтевая студия",
    "Юридические услуги",
    "Магазин автозапчастей и автотоваров",
    "Маркетплейс",
    "Магазин одежды",
    "Барбершоп",
    "Косметология",
    "Ремонт телефонов",
    "Автосалон",
    "Шиномонтаж",
    "Бар, паб",
    "Фитнес-клуб",
    "Доставка еды и обедов",
    "Спортивный клуб, секция",
    "Эпиляция",
    "Автомойка",
    "Окна",
    "Кофейня",
    "Строительная компания",
    "Двери",
    "Агентство недвижимости",
    "Кальян-бар",
    "Информационный интернет-сайт",
    "Парикмахерская",
    "Турагентство",
    "Школа танцев",
    "Компьютерный ремонт и услуги",
    "База, дом отдыха",
    "Детейлинг",
    "Быстрое питание",
    "Эвакуация автомобилей",
    "Дополнительное образование",
    "Мебель на заказ",
    "Массажный салон",
    "Курсы и мастер-классы",
    "Детский сад, ясли",
    "Курсы иностранных языков",
    "Спа-салон",
    "Строительный магазин",
    "Жилой комплекс",
    "Мебель для кухни",
    "Салон бровей и ресниц",
    "Строительные и отделочные работы",
    "Доставка цветов и букетов",
    "Ветеринарная клиника",
    "Магазин табака и курительных принадлежностей",
    "Адвокаты",
    "Магазин мебели",
    "Автошкола",
    "Строительство дачных домов и коттеджей",
    "Баня",
    "Ремонт бытовой техники",
    "Приём и скупка металлолома",
    "Магазин парфюмерии и косметики",
    "Товары для праздника",
    "Организация и проведение детских праздников",
    "Суши-бар",
    "Бухгалтерские услуги",
    "Производственное предприятие",
    "Клининговые услуги",
    "Зоосалон, зоопарикмахерская",
    "Бетон, бетонные изделия",
    "Прокат автомобилей",
    "Магазин сантехники",
    "Пиццерия",
    "Магазин подарков и сувениров",
    "Кузовной ремонт",
    "Металлопрокат",
    "Изготовление памятников и надгробий",
    "Фотоуслуги",
    "Вейп-шоп",
    "Салон оптики",
    "Автомобильные грузоперевозки",
    "Пиломатериалы",
    "Психологическое консультирование",
    "Банкетный зал",
    "Шторы, карнизы",
    "Дизайн интерьеров",
    "Тату-салон",
    "Тара и упаковочные материалы",
    "Магазин электроники",
    "Организация мероприятий",
    "Аренда строительной и спецтехники",
    "Сауна",
    "Хостел",
    "Потолочные системы",
    "Кровля и кровельные материалы",
    "Кондиционеры",
    "Турбаза",
    "Шины и диски",
    "Напольные покрытия",
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

import json
import time
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

citys = ["Казань", "Краснодар", "Курск", "Липецк"]
categories = ["аренда помещений", "автошколы", "развлечения"]

driver = webdriver.Firefox()
all_company_links = {}


def search_category_in_city(city, category):
    try:
        print(f"Поиск в городе: {city}, категория: {category}")
        driver.get("https://yandex.ru/maps")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".input__control"))
        )

        search_box = driver.find_element(By.CSS_SELECTOR, ".input__control")
        search_box.clear()
        search_box.send_keys(f"{city} {category}")
        search_box.send_keys(Keys.RETURN)

        time.sleep(5)

        last_height = driver.execute_script(
            "return document.querySelector('.scroll__container').scrollHeight"
        )
        attempts = 0
        max_attempts = 10

        while attempts < max_attempts:
            elem = driver.find_element(By.CLASS_NAME, "scroll__container")
            elem.send_keys(Keys.END)
            time.sleep(3)

            new_height = driver.execute_script(
                "return document.querySelector('.scroll__container').scrollHeight"
            )
            if new_height == last_height:
                break

            last_height = new_height
            attempts += 1

        page_source = driver.page_source
        tree = etree.fromstring(page_source, etree.HTMLParser())
        all_links = tree.xpath('//a[@class="link-overlay"]/@href')
        company_links = ["https://yandex.ru" + link for link in all_links]

        all_company_links[category] = company_links

    except Exception as e:
        print(f"Ошибка при обработке {city}, {category}: {e}")


for city in citys:
    for category in categories:
        search_category_in_city(city, category)

with open("company_links.json", "w", encoding="utf-8") as file:
    json.dump(all_company_links, file, indent=4, ensure_ascii=False)

driver.quit()

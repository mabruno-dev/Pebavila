import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))
# Resolve module imports

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait

import json
import os
from time import sleep
from threading import Thread
from unidecode import unidecode

from utils.wrappers import timed
from utils.functions import error

running = True

all_addresses = list()

city_url_list = list()

# Retorna as linhas de uma tabela passada por parâmetro
def find_table_rows(table: WebElement):
    table_body = table.find_element(By.TAG_NAME, "tbody")
    return table_body.find_elements(By.TAG_NAME, "tr")

def city_scraper(x: int, y: int):
    global all_addresses
    global city_url_list

    driver = webdriver.Chrome()
    driver.set_window_size(600, 600)
    driver.set_window_position(x + 30, y + 30)

    while len(city_url_list) > 0:
        neighborhood_addresses = list()
        url = city_url_list[0]
        city_url_list.pop(0)
        while True:
            try:
                driver.get(url)

                try:
                    body = driver.find_element(By.TAG_NAME, "body")
                    if "não é uma cidade codificada por logradouros" in body.text:
                        continue
                except:
                    pass

                neighborhood_ul = wait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "column-list"))
                )
                neighborhood_li_list = neighborhood_ul.find_elements(By.TAG_NAME, "li")
                neighborhood_a_list = list()
                for neighborhood_li in neighborhood_li_list:
                    try:
                        neighborhood_a_list.append(neighborhood_li.find_element(By.TAG_NAME, "a").get_attribute("href"))
                    except Exception as e:
                        error(e)

                for neighborhood_a in neighborhood_a_list:
                    driver.get(neighborhood_a)

                    street_tr_list = find_table_rows(
                        wait(driver, 10).until(
                            EC.presence_of_element_located((By.TAG_NAME, "table"))
                        )
                    )

                    for street_tr in street_tr_list:
                        street_td_list = street_tr.find_elements(By.TAG_NAME, "td")
                        address = {
                            "street": unidecode(street_td_list[1].find_element(By.TAG_NAME, "a").text).upper(),
                            "neighborhood": unidecode(street_td_list[3].text.upper()),
                            "city": unidecode(street_td_list[4].text.split("/")[0].upper()),
                            "state": unidecode(street_td_list[4].text.split("/")[1].upper())
                        }
                        print(address)
                        neighborhood_addresses.append(address)
                break
            except Exception as e:
                error(e)
        for item in neighborhood_addresses:
            all_addresses.append(item)

    driver.quit()

@timed
def __main__():
    global all_addresses
    global city_url_list

    driver = webdriver.Chrome()

    driver.get("https://codigo-postal.org/pt-br/brasil/sao-paulo/")

    city_ul = wait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "column-list"))
    )
    city_li_list = city_ul.find_elements(By.TAG_NAME, "li")
    city_a_list = list()
    for city_li in city_li_list:
        try:
            city_a_list.append(city_li.find_element(By.TAG_NAME, "a").get_attribute("href"))
        except Exception as e:
            error(e)

    for city_a in city_a_list:
        city_url_list.append(city_a)

    driver.quit()

    thread_list = list()

    for i in range(10):
        thread = Thread(target=city_scraper, args=(30 * i, 30 * i))
        thread.start()
        thread_list.append(thread)
        sleep(2)

    for thread in thread_list:
        thread.join()

    # Transforma a lista de todos os endereços num JSON
    output_path = r"output"
    os.makedirs(output_path, exist_ok=True)
    json_object = {"addresses": all_addresses}
    with open(output_path + r"/addresses.json", "w") as json_file:
        json.dump(json_object, json_file)


if __name__ == "__main__":
    __main__()
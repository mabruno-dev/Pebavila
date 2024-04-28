import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))
# Resolve module imports

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait

import json
import shutil
import os
import time
from threading import Thread
from unidecode import unidecode

from utils.wrappers import timed
from utils.functions import error

running = True

# Retorna as linhas de uma tabela passada por parâmetro
def find_table_rows(table: WebElement):
    table_body = table.find_element(By.TAG_NAME, "tbody")
    return table_body.find_elements(By.TAG_NAME, "tr")

def write_json(all_addresses: list):
    # Transforma a lista de todos os endereços num JSON
    output_path = r"output"
    file_path = output_path + r"/addresses.json"
    backup_file_path = output_path + r"/addresses_backup.json"

    # Make a backup
    shutil.copy(file_path, backup_file_path)
    
    os.makedirs(output_path, exist_ok=True)
    json_object = {"addresses": all_addresses}
    with open(file_path, "w") as json_file:
        json.dump(json_object, json_file, ensure_ascii=False, indent=4)

def get_progress(all_addresses: list):
    file_path = r"output/addresses.json"
    progress = list()
    if os.path.exists(file_path):
        with open(file_path, "r") as json_file:
            addresses = json.load(json_file)["addresses"]
        for item in addresses:
            all_addresses.append(item)
            temp = f"{item["city"]}/{item["neighborhood"]}"
            if not temp in progress:
                progress.append(temp)
                if "º" in temp:
                    progress.append(temp.replace("º", "o"))

    return progress
        
def replace_degree(s: str):
    try:
        if s[s.find("deg") - 1].isdigit():
            return s.replace("deg", "º")
    except:
        pass
    return s

def progress_saver(all_addresses: list):
        global running

        while running:
            write_json(all_addresses)
            for _ in range(300):
                if not running:
                    break
                time.sleep(1)

def get_url_dont_wait(driver: webdriver.Chrome, url: str):
    got_url = False

    def get_url():
        nonlocal got_url
        try:
            driver.get(url)
            got_url = True
        except:
            pass

    thread = Thread(target=get_url)
    thread.start()
    start = time.time()
    while not got_url:
        if time.time() - start > 30:
            driver.quit()
            time.sleep(3)
            driver = webdriver.Chrome()
            print("driver.get took too long")
            get_url_dont_wait(driver, url)
            break

@timed
def __main__():
    global running

    all_addresses = list() 

    progress_list = get_progress(all_addresses)

    thread = Thread(target=progress_saver, args=(all_addresses,))
    thread.start()

    driver = webdriver.Chrome()

    driver.get("https://codigo-postal.org/pt-br/brasil/sao-paulo/")

    city_ul = wait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "column-list"))
    )
    city_li_list = city_ul.find_elements(By.TAG_NAME, "li")
    city_list = list()
    for city_li in city_li_list:
        try:
            city_a = city_li.find_element(By.TAG_NAME, "a")
            city_list.append({
                "name": city_a.text,
                "url": city_a.get_attribute("href")
            })

        except Exception as e:
            error(e)

    for city in city_list:
        while True:
            try:
                get_url_dont_wait(driver, city["url"])

                try:
                    body = wait(driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                    if "não é uma cidade codificada por logradouros" in body.text:
                        break
                    elif "Página no encontrada" in body.text:
                        break
                except:
                    pass

                neighborhood_ul = wait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "column-list"))
                )
                neighborhood_li_list = neighborhood_ul.find_elements(By.TAG_NAME, "li")
                neighborhood_list = list()
                for neighborhood_li in neighborhood_li_list:
                    try:
                        neighborhood_a = neighborhood_li.find_element(By.TAG_NAME, "a")
                        neighborhood_list.append({
                            "name": neighborhood_a.text,
                            "url": neighborhood_a.get_attribute("href")
                        })
                    except Exception as e:
                        error(e)

                for neighborhood in neighborhood_list:
                    
                    cn_str = replace_degree(unidecode(f"{city["name"]}/{neighborhood["name"]}").upper()).split("(")[0].strip()
                    if cn_str in progress_list:
                        continue

                    while True:
                        try:
                            get_url_dont_wait(driver, neighborhood["url"])

                            street_tr_list = find_table_rows(
                                wait(driver, 10).until(
                                    EC.presence_of_element_located((By.TAG_NAME, "table"))
                                )
                            )

                            for street_tr in street_tr_list:
                                street_td_list = street_tr.find_elements(By.TAG_NAME, "td")
                                address = {
                                    "street": unidecode(street_td_list[1].find_element(By.TAG_NAME, "a").text).upper(),
                                    "neighborhood": replace_degree(unidecode(street_td_list[3].text.upper())).split("(")[0].strip(),
                                    "city": unidecode(street_td_list[4].text.split("/")[0].upper()),
                                    "state": unidecode(street_td_list[4].text.split("/")[1].upper())
                                }
                                print(address)
                                all_addresses.append(address)
                            break
                        except Exception as e:
                            error(e)
                break
            except Exception as e:
                error(e)

    write_json(all_addresses)

    driver.quit()

    running = False
    thread.join()


if __name__ == "__main__":
    __main__()
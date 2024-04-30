import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))
# Resolve module imports

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait

import os
import json
import time
import shutil
from threading import Thread
from unidecode import unidecode

from utils.wrappers import timed
from utils.functions import error

running = True

CURRENT_STATE = "SP"

# Retorna as linhas de uma tabela passada por parâmetro
def find_table_rows(table: WebElement):
    table_body = table.find_element(By.TAG_NAME, "tbody")
    return table_body.find_elements(By.TAG_NAME, "tr")

def backup_json():
    output_path = r"output"
    file_path = output_path + r"/addresses.json"
    backup_file_path = output_path + r"/addresses_backup.json"
    shutil.copy(file_path, backup_file_path)

def write_json(all_addresses: dict):
    output_path = r"output"
    file_path = output_path + r"/addresses.json"
    
    os.makedirs(output_path, exist_ok=True)
    json_object = {"addresses": all_addresses}
    with open(file_path, "w") as json_file:
        json.dump(json_object, json_file, ensure_ascii=False, indent=4)

def remove_deg(s: str):
    for i in range(1, 10):
        s = s.replace(f"{i}DEG", str(i))
        s = s.replace(f"{i}ADEG", str(i))
        s = s.replace(f"{i}deg", str(i))
        s = s.replace(f"{i}adeg", str(i))
        s = s.replace(f"{i}O", str(i))
        s = s.replace(f"{i}o", str(i))
    return s

def normalize_str(s: str):
    s = s.upper()
    s = s.strip()
    s = s.split("(")[0]
    s = unidecode(s)
    s = remove_deg(s)
    return s

def get_progress():
    file_path = r"output/addresses.json"
    progress = list()
    if os.path.exists(file_path):
        with open(file_path, "r") as json_file:
            all_addresses = json.load(json_file)

        for key1 in all_addresses.keys():
            for key2 in all_addresses[key1].keys():
                for key3 in all_addresses[key1][key2].keys():
                        progress.append(f"{key2}/{key3}")
    # print(all_addresses)
    return all_addresses, progress

def progress_saver(all_addresses: dict):
        global running

        list_len = len(all_addresses)
        while running:
            backup_json()
            if list_len != len(all_addresses):
                list_len = len(all_addresses)
                write_json(all_addresses)
                time.sleep(300)

def get_next_city(all_addresses: dict):
    cities_list = list(all_addresses[CURRENT_STATE].keys())
    cities_list.sort()
    return cities_list[-1]

@timed
def __main__():
    global running

    all_addresses, progress_list = get_progress()

    get_next_city(all_addresses) 

    thread = Thread(target=progress_saver, args=(all_addresses,))
    thread.start()

    driver = webdriver.Chrome()
    driver.set_page_load_timeout(10)

    while True:
        try:
            driver.get("https://codigo-postal.org/pt-br/brasil/sao-paulo/")
            break
        except:
            print("Connection failed, trying again")

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

    next_city = get_next_city(all_addresses)

    for city in city_list:
        if next_city:
            if normalize_str(city["name"]) == next_city:
                next_city = None
            else:
                continue    

        while True:
            try:
                driver.get(city["url"])

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
                    
                    cn_str = normalize_str(f"{city["name"]}/{neighborhood["name"]}")
                    if cn_str in progress_list:
                        continue

                    while True:
                        try:
                            if neighborhood["url"] == city["url"] + "/":
                                break

                            driver.get(neighborhood["url"])

                            street_tr_list = find_table_rows(
                                wait(driver, 10).until(
                                    EC.presence_of_element_located((By.TAG_NAME, "table"))
                                )
                            )

                            for street_tr in street_tr_list:
                                street_td_list = street_tr.find_elements(By.TAG_NAME, "td")
                                address = {
                                    "street": normalize_str(street_td_list[1].find_element(By.TAG_NAME, "a").text),
                                    "neighborhood": normalize_str(street_td_list[3].text),
                                    "city": normalize_str(street_td_list[4].text.split("/")[0]),
                                    "state": normalize_str(street_td_list[4].text.split("/")[1])
                                }
                                print(address)
                                if address["state"] not in all_addresses.keys():
                                    all_addresses[address["state"]] = {}
                                if address["city"] not in all_addresses[address["state"]].keys():
                                    all_addresses[address["state"]][address["city"]] = {}
                                if address["neighborhood"] not in all_addresses[address["state"]][address["city"]].keys():
                                    all_addresses[address["state"]][address["city"]][address["neighborhood"]] = []
                                if address["street"] not in all_addresses[address["state"]][address["city"]][address["neighborhood"]]:
                                    all_addresses[address["state"]][address["city"]][address["neighborhood"]].append(address["street"])
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
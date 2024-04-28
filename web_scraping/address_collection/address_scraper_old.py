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
from unidecode import unidecode

from utils.wrappers import timed
from utils.functions import error

# Retorna as linhas de uma tabela passada por parâmetro
def find_table_rows(table: WebElement):
    table_body = table.find_element(By.TAG_NAME, "tbody")
    return table_body.find_elements(By.TAG_NAME, "tr")

def write_json(all_addresses: list):
    # Transforma a lista de todos os endereços num JSON
    output_path = r"output"
    os.makedirs(output_path, exist_ok=True)
    json_object = {"addresses": all_addresses}
    with open(output_path + r"/addresses.json", "w") as json_file:
        json.dump(json_object, json_file, indent=4)

def get_progress(all_addresses: list):
    file_path = r"output/addresses.json"
    progress = list()
    if os.path.exists(file_path):
        with open(file_path, "r") as json_file:
            addresses = json.load(json_file)["addresses"]
        for item in addresses:
            all_addresses.append(item)
            if not f"{item["city"]}/{item["neighborhood"]}" in progress:
                progress.append(f"{item["city"]}/{item["neighborhood"]}")
    return progress
        
def replace_degree(s: str):
    if s[s.find("deg") - 1].isdigit():
        return s.replace("deg", "º")
    return s

@timed
def __main__():
    all_addresses = list()

    progress_list = get_progress(all_addresses)

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
        
        driver.get(city["url"])

        try:
            body = wait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            if "não é uma cidade codificada por logradouros" in body.text:
                continue
        except:
            pass

        try:
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
                
                driver.get(neighborhood["url"])

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
            
                write_json(all_addresses)

        except Exception as e:
            error(e)

    driver.quit()


if __name__ == "__main__":
    __main__()
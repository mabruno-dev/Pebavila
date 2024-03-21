from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait

from time import sleep
import json
import os
from unidecode import unidecode

# Retorna as linhas de uma tabela passada por parâmetro
def find_table_rows(table: WebElement):
    table_body = table.find_element(By.TAG_NAME, "tbody")
    return table_body.find_elements(By.TAG_NAME, "tr")

def __main__():
    all_addresses = list()

    driver = webdriver.Safari()

    driver.get("https://codigo-postal.org/pt-br/brasil/rio-de-janeiro/")

    city_ul = wait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "column-list"))
    )
    city_li_list = city_ul.find_elements(By.TAG_NAME, "li")
    city_a_list = list()
    for city_li in city_li_list:
        try:
            city_a_list.append(city_li.find_element(By.TAG_NAME, "a").get_attribute("href"))
        except Exception as e:
            print(f"Error: {e}")

    for city_a in city_a_list:
        
        driver.get(city_a)

        try:
            neighborhood_ul = wait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "column-list"))
            )
            neighborhood_li_list = neighborhood_ul.find_elements(By.TAG_NAME, "li")
            neighborhood_a_list = list()
            for neighborhood_li in neighborhood_li_list:
                try:
                    neighborhood_a_list.append(neighborhood_li.find_element(By.TAG_NAME, "a").get_attribute("href"))
                except Exception as e:
                    print(f"Error: {e}")

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
                    all_addresses.append(address)

        except Exception as e:
            print(f"Error: {e}")

    driver.quit()

    # Transforma a lista de todos os endereços num JSON
    output_path = r"output"
    os.makedirs(output_path, exist_ok=True)
    json_object = {"addresses": all_addresses}
    with open(output_path + r"/addresses.json", "w") as json_file:
        json.dump(json_object, json_file)


if __name__ == "__main__":
    __main__()
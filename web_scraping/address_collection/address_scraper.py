from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
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

    driver = webdriver.Chrome()
    driver.get("https://codigo-postal.org/pt-br/brasil/rj/niteroi/")
    sleep(5)

    # As variaveis são nomeadas a partir do grupo encontrado na paágina e da tag
    neighborhood_ul = driver.find_element(By.CLASS_NAME, "column-list")
    neighborhood_li_list = neighborhood_ul.find_elements(By.TAG_NAME, "li")

    # Percorre cada um dos bairros
    for neighborhood_li in neighborhood_li_list:
        neighbordhood_a = neighborhood_li.find_element(By.TAG_NAME, "a")
        driver.get(neighbordhood_a.get_attribute("href"))
        street_tr_list = find_table_rows(
            driver.find_element(By.TAG_NAME, "table"))

        # Percorre cada uma das ruas
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

        driver.back()
        sleep(5)

    driver.quit()

    # Transforma a lista de todos os endereços num JSON
    output_path = r"output"
    os.makedirs(output_path)
    json_object = {"addresses": all_addresses}
    with open(output_path + r"/addresses.json", "w") as json_file:
        json.dump(json_object, json_file)


if __name__ == "__main__":
    __main__()
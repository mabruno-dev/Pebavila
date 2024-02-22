import os
import sys

current_file = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file)
project_root = os.path.dirname(current_directory)
sys.path.append(project_root)

import json
from re import findall
from time import sleep

from unidecode import unidecode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth

from utils.constants import RealtyConstants as RC
from utils.functions import print_log

def find_numbers(s: str):
    result = findall(r"\d+\.*\d*", s)
    # O padrão de expressão regular r'\d+\.*\d*' corresponde a um ou mais dígitos \d+,
    # seguido de um ponto opcional \.* e zero ou mais dígitos \d*.
    # Este padrão permite corresponder a números inteiros e decimais.
    return result if len(result) > 0 else [None]
    
def is_number(s: str):
    return s.isdigit()

def scrape_realty(url):

    driver = webdriver.Chrome()

    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    
    driver.get(url)

    try:
        status_span = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "main__labels"))
        )
    except:
        print("Connection error")
        driver.quit()
        return scrape_realty(url)

    if "Em construção" in status_span.text:
        status = RC.UNDER_CONSTRUCTION
    elif "Na planta" in status_span.text:
        status = RC.FLOOR_PLAN
    else:
        status = RC.DONE

    name = driver.find_element(By.CLASS_NAME,  "info__business-type")
    type = unidecode(name.text.split("para")[0].strip().upper())

    location_button = driver.find_element(By.CLASS_NAME, "info__map-link")
    location = location_button.text.replace("pin", "").replace(",", "$").replace(" - ", "$").replace("\n", "")
    location_list = location.split("$")
    for index, item in enumerate(location_list):
        location_list[index] = item.strip()
    match(len(location_list)):
        case 5:
            street = location_list[0]
            number = location_list[1]
            neighborhood = location_list[2]
            city = location_list[3]
            state = location_list[4]
        case 4:
            street = None
            number = location_list[0]
            neighborhood = location_list[1]
            city = location_list[2]
            state = location_list[3]
        case 3:
            street = None
            number = None
            neighborhood = location_list[0]
            city = location_list[1]
            state = location_list[2]
        case _:
            print(f"Error scraping location\nurl: {url}")
            return

    price_div = driver.find_element(By.CLASS_NAME, "prices__container")
    try:
        price = float(find_numbers(price_div.text.replace(".", ""))[0])

    except:
        print("Price not informed, skipping realty") # Normalmente sob consulta
        return
    try:
        price_ul = price_div.find_element(By.TAG_NAME, "ul")
        price_li_list = price_ul.find_elements(By.TAG_NAME, "li")
        for price_li in price_li_list:

            if "condomínio" in price_li.text:
                condo_price = float(find_numbers(price_li.text)[0])
            else:
                print("Condo price not informed")
                condo_price = None

            if "IPTU" in price_li.text:
                property_tax = float(find_numbers(price_li.text)[0])
            else:
                print("Taxes not informed")
                property_tax = None
    except:
        print("Condo price and taxes not informed")
        condo_price = None
        property_tax = None

    # Coleta os valores mais baixos
    features_ul = driver.find_element(By.CLASS_NAME, "info__base-amenities")
    try:
        square_footage = int(find_numbers(features_ul.find_element(By.CSS_SELECTOR, 'span[itemprop="floorSize"]').text)[0])
    except:
        print("Square footage not informed")
        square_footage = None
    try:
        bedrooms = int(find_numbers(features_ul.find_element(By.CSS_SELECTOR, 'span[itemprop="numberOfRooms"]').text)[0])
    except:
        print("Number of bedrooms not informed")
        bedrooms = None
    try:
        parking_spaces = int(find_numbers(features_ul.find_element(By.CLASS_NAME, "js-parking-spaces").text)[0])
    except:
        print("Number of parking spaces not informed")
        parking_spaces = None
    try:
        bathrooms = int(find_numbers(features_ul.find_element(By.CSS_SELECTOR, 'span[itemprop="numberOfBathroomsTotal"]').text)[0])
    except:
        print("Number of bathrooms not informed")
        bathrooms = None
    try:
        floor = int(find_numbers(features_ul.find_element(By.CSS_SELECTOR, 'span[itemprop="floorLevel"]').text)[0])
    except:
        print("Floor not informed")
        floor = None

    advertiser_div = driver.find_element(By.CLASS_NAME, "advertser-info--wrapper")
    advertiser_name = unidecode(advertiser_div.find_element(By.CLASS_NAME, "advertiser-info__name").text.strip().upper())

    # Descrição deve ser conservada para exibição ao usuário caso necessária
    description = driver.find_element(By.CLASS_NAME, "amenities__description").text.strip()

    if "mobiliado" in url:
        furnished = RC.FURNISHED
    else:
        furnished = RC.NOT_FURNISHED

    # Huge gibberish is to ensure that the variables are the right type and not try to cast a null variable
    realty_dict = {
        "realty_location": {
            "state": str(state) if state else None,
            "city": str(city) if city else None,
            "neighborhood": str(neighborhood) if neighborhood else None,
            "street": str(street) if street else None
        },
        "realty_number": str(number) if number else None,
        "realty_square_footage": int(square_footage) if square_footage else None,
        "realty_price": float(price) if price else None,
        "realty_description": str(description) if description else None,
        "realty_parking_spaces": int(parking_spaces) if parking_spaces else None,
        "realty_bathrooms": int(bathrooms) if bathrooms else None,
        "realty_bedrooms": int(bedrooms) if bedrooms else None,
        "realty_advertiser": str(advertiser_name) if advertiser_name else None,
        "realty_done": int(status) if status else None,
        "realty_property_tax": float(property_tax) if property_tax else None,
        "realty_furnished": str(furnished) if furnished else None,
        "realty_condo_price": float(condo_price) if condo_price else None,
        "realty_floor": int(floor) if floor else None,
        "realty_type": str(type) if type else None,
        "realty_url": str(url) if url else None
    }


    print(f"{json.dumps(realty_dict, indent=4, ensure_ascii=False)}")
    print_log(f"Scraped realty: {name.text}", showCons=False)

    return realty_dict


def __main__():
    print(scrape_realty("https://www.zapimoveis.com.br/imovel/venda-terreno-lote-condominio-itaipu-niteroi-rj-1400m2-id-2665924421/?"))

if __name__ == "__main__":
    __main__()
import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))
# Resolve module imports

import json
from re import findall
import inspect
import requests
import base64
from time import sleep

from unidecode import unidecode
import undetected_chromedriver as uc
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from utils.constants import RealtyConstants as RC
from utils.functions import print_log
from utils.wrappers import timed

frame = inspect.stack()[-1]
dir_path = "/".join(frame.filename.replace("\\", "/").split("/")[:-1]).replace("/_internal", "")

# JSON_PATH = os.path.join(dir_path, "output/status.json")

class InvalidStatusKeyException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def verify_human(driver: webdriver, wait: WebDriverWait):
    try:
        title = driver.find_element(By.CLASS_NAME, "zone-name-title h1")
        if "zapimoveis" in title.text:
            print("verificando")
            checkbox = wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "input"))
            )
            checkbox.click()
            sleep(10)
    except:
        print("no verification needed")

# def set_status(**kwargs):
#     with open(JSON_PATH, "r", encoding="utf-8") as json_file:
#         status = json.load(json_file)
#         for key, value in kwargs.items():
#             if key in status:
#                 status[key] = value
#             else:
#                 raise InvalidStatusKeyException(f'"{key}" is not a valid status.')
            
#     with open(JSON_PATH, "w", encoding="utf-8") as json_file:
#         json.dump(status, json_file, indent=4, ensure_ascii=False)

def find_numbers(s: str):
    result = findall(r"\d+\.*\d*", s)
    # O padrão de expressão regular r'\d+\.*\d*' corresponde a um ou mais dígitos \d+,
    # seguido de um ponto opcional \.* e zero ou mais dígitos \d*.
    # Este padrão permite corresponder a números inteiros e decimais.
    return result if len(result) > 0 else [None]
    
def is_number(s: str):
    return s.isdigit()

def set_driver_options():
    options = webdriver.ChromeOptions()
    
    # # Set up a temporary directory for user data
    # options.add_argument('--user-data-dir=/tmp/chrome_user_data')

    # # Disable cache
    # options.add_argument('--disable-application-cache')
    # options.add_argument('--disk-cache-dir=/dev/null')

    # Set log level to mininum
    options.add_argument('--log-level=3')

    # Enable incognito mode
    options.add_argument('--incognito')

    return options

@timed
def scrape_realty(driver: webdriver, url: str):
    
    wait = WebDriverWait(driver, 10)

    driver.get(url)

    try:
        # verify_human(driver, wait)
        status_span = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "main__labels"))
        )
    except:
        print("Connection error")
        driver.quit()
        sleep(15)
        driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=set_driver_options())
        return scrape_realty(driver, url)

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
            street = unidecode(location_list[0].upper())
            number = unidecode(location_list[1].upper())
            neighborhood = unidecode(location_list[2].upper())
            city = unidecode(location_list[3].upper())
            state = unidecode(location_list[4].upper())
        case 4:
            street = unidecode(location_list[0].upper())
            number = None
            neighborhood = unidecode(location_list[1].upper())
            city = unidecode(location_list[2].upper())
            state = unidecode(location_list[3].upper())
        case 3:
            street = None
            number = None
            neighborhood = unidecode(location_list[0].upper())
            city = unidecode(location_list[1].upper())
            state = unidecode(location_list[2].upper())
        case _:
            print(f"Error scraping location\nurl: {url}")
            return

    price_div = driver.find_element(By.CLASS_NAME, "prices__container")
    try:
        price = find_numbers(price_div.text.replace(".", ""))[0]

    except:
        print("Price not informed, skipping realty") # Normalmente sob consulta
        return
    try:
        price_ul = price_div.find_element(By.CLASS_NAME, "subinfo")
        price_li_list = price_ul.find_elements(By.TAG_NAME, "li")
        condo_price = None
        property_tax = None
        for price_li in price_li_list:
            if "condomínio" in price_li.text:
                condo_price = find_numbers(price_li.text.replace(".", ""))[0]

            if "IPTU" in price_li.text:
                property_tax = find_numbers(price_li.text.replace(".", ""))[0]

        if not condo_price:
            print("Condo price not informed")
        if not property_tax:
            print("Property tax not informed")
    except:
        print("Condo price and taxes not informed")
        condo_price = None
        property_tax = None
    

    # Coleta os valores mais baixos
    features_ul = driver.find_element(By.CLASS_NAME, "info__base-amenities")
    try:
        square_footage = find_numbers(features_ul.find_element(By.CSS_SELECTOR, 'span[itemprop="floorSize"]').text)[0]
    except:
        print("Square footage not informed")
        square_footage = None
    try:
        bedrooms = find_numbers(features_ul.find_element(By.CSS_SELECTOR, 'span[itemprop="numberOfRooms"]').text)[0]
    except:
        print("Number of bedrooms not informed")
        bedrooms = None
    try:
        parking_spaces = find_numbers(features_ul.find_element(By.CLASS_NAME, "js-parking-spaces").text)[0]
    except:
        print("Number of parking spaces not informed")
        parking_spaces = None
    try:
        bathrooms = find_numbers(features_ul.find_element(By.CSS_SELECTOR, 'span[itemprop="numberOfBathroomsTotal"]').text)[0]
    except:
        print("Number of bathrooms not informed")
        bathrooms = None
    try:
        floor = find_numbers(features_ul.find_element(By.CSS_SELECTOR, 'span[itemprop="floorLevel"]').text)[0]
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
            "state": str(state),
            "city": str(city),
            "neighborhood": str(neighborhood),
            "street": str(street) if street else None
        },
        "realty_number": str(number) if number else None,
        "realty_square_footage": int(square_footage) if square_footage else None,
        "realty_price": float(price),
        "realty_property_tax": float(property_tax) if property_tax else None,
        "realty_condo_price": float(condo_price) if condo_price else None,
        "realty_description": str(description),
        "realty_parking_spaces": int(parking_spaces) if parking_spaces else None,
        "realty_bathrooms": int(bathrooms) if bathrooms else None,
        "realty_bedrooms": int(bedrooms) if bedrooms else None,
        "realty_advertiser": str(advertiser_name) if advertiser_name else None,
        "realty_status": int(status),
        "realty_furnished": bool(furnished),
        "realty_floor": int(floor) if floor else None,
        "realty_type": str(type),
        "realty_url": str(url)
    }

    formatted_dict = realty_dict.copy()
    if len(realty_dict["realty_description"]) > 70:
        formatted_dict["realty_description"] = realty_dict["realty_description"][:70].strip() + "..."
    print("Data: ", end="")
    print(json.dumps(formatted_dict, indent=4, ensure_ascii=False))

    return realty_dict

# Main function for testing purposes
def __main__():
    options = webdriver.ChromeOptions()
    
    # # Set up a temporary directory for user data
    # options.add_argument('--user-data-dir=/tmp/chrome_user_data')

    # # Disable cache
    # options.add_argument('--disable-application-cache')
    # options.add_argument('--disk-cache-dir=/dev/null')

    # Set log level to mininum
    options.add_argument('--log-level=3')

    # Enable incognito mode
    options.add_argument('--incognito')

    driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    scrape_realty("https://www.zapimoveis.com.br/lancamento/venda-apartamento-2-quartos-sao-lourenco-niteroi-rj-279m2-id-2646116981/")

if __name__ == "__main__":
    __main__()
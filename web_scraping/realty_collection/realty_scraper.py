import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))
# Resolve module imports

from re import findall
import inspect

from unidecode import unidecode
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.constants import RealtyConstants as RC
from utils.wrappers import timed

frame = inspect.stack()[-1]
dir_path = "/".join(frame.filename.replace("\\", "/").split("/")[:-1]).replace("/_internal", "")

# JSON_PATH = os.path.join(dir_path, "output/status.json")

class InvalidStatusKeyException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

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

    # Disable cache
    options.add_argument('--disable-application-cache')
    options.add_argument('--disk-cache-dir=/dev/null')

    # Set log level to mininum
    options.add_argument('--log-level=3')

    # Enable incognito mode
    options.add_argument('--incognito')

    return options  

def get_type(s: str):
    first_nuber = find_numbers(s)[0]
    print(first_nuber)
    if f"{first_nuber} quartos" in s:
        type = unidecode(s.split("com")[0].strip().upper())
    else:
        type = unidecode(s.split(str(first_nuber))[0].strip().upper())
    return type

@timed
def scrape_realty(driver: webdriver.Chrome, url: str):
    
    wait = WebDriverWait(driver, 10)

    driver.get(url)

    body = driver.find_element(By.TAG_NAME, "body")
    if "Performance & security by Cloudflare" in body.text:
        return scrape_realty(driver, url)

    try:
        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "price-info-value"))
        )
    except:
        print("Connection error")
        return scrape_realty(driver, url)

    try:
        status_span = driver.find_element(By.CLASS_NAME, "details-content__info-tags")
        if "Em construção" in status_span.text:
            status = RC.UNDER_CONSTRUCTION
        elif "Na planta" in status_span.text:
            status = RC.FLOOR_PLAN
        else:
            status = RC.DONE
    except:
        status = RC.DONE

    # type_info = driver.find_elements(By.CLASS_NAME, "l-breadcrumb l-breadcrumb--small l-breadcrumb--collapsed")
    # if "Lançamentos" in type_info[0].text:
    #     type = unidecode(type_info[0].text.split("de")[1].strip().replace("s/", "").upper())
    # elif "à Venda" in type_info[0].text:
    #     type = unidecode(type_info[0].text.split("à")[0].replace("s ", " ").strip().upper())
    # else:
    #     pass

    location_button = driver.find_element(By.CLASS_NAME, "address-info-value")
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
    
    description_h1_list = driver.find_elements(By.CLASS_NAME, "description__title")
    for item in description_h1_list:
        if item.text:
            description_h1 = item
            break
    type = get_type(description_h1.text)

    price_div = driver.find_element(By.CLASS_NAME, "price-info-value")
    try:
        price = find_numbers(price_div.text.replace(".", ""))[0]

    except:
        print("Price not informed, skipping realty") # Normalmente sob consulta
        return
    
    additional_price_info = driver.find_element(By.CLASS_NAME, "additional-price-info")
    additional_price_elements = additional_price_info.find_elements(By.TAG_NAME, "p")
    for item in additional_price_elements:
        if "Condomínio" in item.text:
            condo_price = find_numbers(item.text.replace(".", ""))[0]
        elif "IPTU" in item.text:
            property_tax = find_numbers(item.text.replace(".", ""))[0]
    if not condo_price:
        print("Condo price not informed")
    if not property_tax:
        print("Property tax not informed")

    # Coleta os valores mais baixos
    features_ul = driver.find_element(By.CLASS_NAME, "amenities-list")
    try:
        square_footage = find_numbers(features_ul.find_element(By.CSS_SELECTOR, 'p[itemprop="floorSize"]').text)[0]
    except:
        print("Square footage not informed")
        square_footage = None
    try:
        bedrooms = find_numbers(features_ul.find_element(By.CSS_SELECTOR, 'p[itemprop="numberOfRooms"]').text)[0]
    except:
        print("Number of bedrooms not informed")
        bedrooms = None
    try:
        parking_spaces = find_numbers(features_ul.find_element(By.CSS_SELECTOR, 'p[itemprop="numberOfParkingSpaces"]').text)[0]
    except Exception as e:
        print("Number of parking spaces not informed")
        parking_spaces = None
    try:
        bathrooms = find_numbers(features_ul.find_element(By.CSS_SELECTOR, 'p[itemprop="numberOfBathroomsTotal"]').text)[0]
    except:
        print("Number of bathrooms not informed")
        bathrooms = None
    try:
        floor = find_numbers(features_ul.find_element(By.CSS_SELECTOR, 'p[itemprop="floorLevel"]').text)[0]
    except:
        print("Floor not informed")
        floor = None

    advertiser_div = driver.find_elements(By.CLASS_NAME, "advertiser-info__credentials")[1]
    advertiser_name = unidecode(advertiser_div.text.strip().upper())

    # Descrição deve ser conservada para exibição ao usuário caso necessária
    description = driver.find_element(By.CLASS_NAME, "description__content--text").text.strip()

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

    return realty_dict

# Main function for testing purposes
def __main__():
    driver = uc.Chrome(options=set_driver_options())
    print(scrape_realty(driver, "https://www.zapimoveis.com.br/imovel/venda-terreno-lote-condominio-portao-curitiba-pr-587m2-id-2713268416/"))

if __name__ == "__main__":
    __main__()
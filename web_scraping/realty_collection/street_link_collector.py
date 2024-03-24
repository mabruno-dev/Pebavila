import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))
# Resolve module imports

from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from unidecode import unidecode

from time import sleep
import random
from datetime import datetime

from utils.wrappers import timed
from database.connection import Database
from database.functions.zapimoveis import *
from database.functions.public import *
from utils.constants import ConsoleColors as Console

database = Database(ensure_connection=True)

def get_address_url(driver: webdriver.Chrome, location: dict, update = False):

    global database
    
    address = f"{location['street']}, {location['city']} - {location['state']}"
    address = address.replace("'", "")

    if not check_address_url_exists(database, {"address": address, "url": None}) or update:

        print(Console.BOLD_WHITE + f"Getting url from address: {address}" + Console.RESET)

        while True:
            try:
                text_input = Wait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Digite o nome da rua, bairro ou cidade"]')))
                text_input.click()
                break
            except:
                continue

        def clear_inputs():
            text_input.click()
            if sys.platform.startswith('darwin'):
                text_input.send_keys(Keys.COMMAND, "a")
            else:
                text_input.send_keys(Keys.CONTROL, "a")
            text_input.send_keys("-" * 10)
            while True:
                try:
                    driver.find_element(By.CSS_SELECTOR, '[data-cy="locations-item-input"]')
                except:
                    break
            text_input.send_keys(Keys.BACKSPACE * 10)

        while True:
            try:
                driver.execute_script(f"arguments[0].value = '{address}';", text_input)
                text_input.send_keys(Keys.SPACE)
                break
            except Exception as e:
                print(f"Error: {e}\nTrying again...")

        while True:
            try:
                location_div = Wait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-cy="locations-item-input"]')))
                print(unidecode(location_div.text.upper()))
                print(address)
                if unidecode(location_div.text.upper()) != address:
                    print(Console.RED + "No results  " + Console.RESET)
                    clear_inputs()
                    while True:
                        try:
                            driver.find(By.CSS_SELECTOR, '[data-cy="locations-item-input"]')
                        except:
                            break
                    return {
                        "address": address,
                        "url": None
                    }
                break
            except:
                try:
                    driver.find_element(By.CLASS_NAME, "locations-feedback") # Tries to find the "not found" element
                    print(Console.RED + "No results  " + Console.RESET)
                    clear_inputs()
                    return {
                        "address": address,
                        "url": None
                    }
                except:
                    try:
                        driver.find_element(By.CSS_SELECTOR, 'a[class="multiselect__redirect"]') # Tries to find the first element of "Imobiliárias"
                        print(Console.RED + "No results  " + Console.RESET)
                        clear_inputs()
                        return {
                            "address": address,
                            "url": None
                        }
                    except:
                        print("Searching...", end="\r")
        
        location_div.click()

        while not (
            location["state"].lower() in driver.current_url and
            location["city"].lower().replace(" ", "-") in driver.current_url and
            location["street"].lower().replace(" ", "-") in driver.current_url
        ):
            sleep(0.1)

        street_url = driver.current_url

        clear_button = Wait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "search-multiselect__clean-button")))
        clear_button.click()

        while driver.current_url != street_url:
            sleep(0.1)

        clear_inputs()

        print(Console.GREEN + "Success: " + Console.RESET + f"{street_url}")

        return {
            "address": address,
            "url": street_url
        }
    else:
        print(Console.BLUE + "Skipped " + Console.RESET + f"{address}")

def fix_nullified_urls(driver: webdriver):
    print("Fixing nullified")
    result = database.query(
        "SELECT address FROM zapimoveis.address_urls WHERE updated_at >= %s AND updated_at < %s AND url IS NULL",
        (datetime(2024, 3, 23, 16, 0), datetime(2024, 4, 23, 2, 0))
    )
    if result:
        for item in result:
            address = item[0]
            street_and_city, state = address.split(" - ")
            street, city = street_and_city.split(", ")
            location = {
                "state": state,
                "city": city,
                "neighborhood": None,
                "street": street
            }
            address_url = get_address_url(driver, location, update=True)
            if address_url:
                update_address_url(database, address_url)

def fix_unwanted_urls(driver: webdriver):
    print("Fixing wrong addresses")
    result = database.query(
        "SELECT address, url FROM zapimoveis.address_urls WHERE url IS NOT NULL"
    )
    if result:
        addresses = list()

        for item in result:
            address = item[0]
            url = item[1]
            street_and_city, state = address.split(" - ")
            street, city = street_and_city.split(", ")
            location = {
                "state": state,
                "city": city,
                "neighborhood": None,
                "street": street
            }
            if not (
                location["state"].lower() in url and
                location["city"].lower().replace(" ", "-") in url and
                location["street"].lower().replace(" ", "-") in url
            ):
                addresses.append(item)

        for item in addresses:
            address = item[0]
            street_and_city, state = address.split(" - ")
            street, city = street_and_city.split(", ")
            location = {
                "state": state,
                "city": city,
                "neighborhood": None,
                "street": street
            }
            address_url = get_address_url(driver, location, update=True)
            if address_url:
                update_address_url(database, address_url)

@timed
def __main__():

    global database

    options = webdriver.ChromeOptions()
    options.add_argument('--log-level=3')

    driver = webdriver.Chrome(options=options)

    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    driver.get("https://www.zapimoveis.com.br/venda/?itl_id=1000063&itl_name=zap_-_link-header_comprar_to_zap_resultado-pesquisa")

    fix_nullified_urls(driver)
    fix_unwanted_urls(driver)

    cities = get_all_cities(database)
    for city in cities:
        locations = get_locations_from_city(database, city["city_name"], "RJ")

        for index, location in enumerate(locations):
            print(Console.BLACK + f"{index + 1}/{len(locations)}" + Console.RESET, end=" ")
            address_url = get_address_url(driver, location)
            if address_url:
                insert_address_url(database, address_url)
                
    driver.quit()

if __name__ == "__main__":
    __main__()
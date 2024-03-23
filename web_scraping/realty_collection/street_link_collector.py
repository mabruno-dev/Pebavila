import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))
# Resolve module imports

from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep
import random

from utils.wrappers import timed
from database.connection import Database
from database import functions as db_functions
from utils.constants import ConsoleColors as Console

database = Database(ensure_connection=True)

def get_address_url(driver: webdriver.Chrome, location: dict, update = False):

    global database
    
    address = f"{location['street']}, {location['city']} - {location['state']}"
    address = address.replace("'", "")

    if not (db_functions.Zapimoveis.check_address_url_exists(database, {"address": address, "url": None}) or update):
        print(Console.BOLD_WHITE + f"Getting url from address: {address}" + Console.RESET)

        text_input = Wait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Digite o nome da rua, bairro ou cidade"]')))

        text_input.click()
        while True:
            try:
                sleep(1)
                driver.execute_script(f"arguments[0].value = '{address}';", text_input)
                text_input.send_keys(Keys.SPACE)
                break
            except Exception as e:
                print(f"Error: {e}\nTrying again...")

        while True:
            try:
                location_div = Wait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-cy="locations-item-input"]')))
                break
            except:
                try:
                    driver.find_element(By.CLASS_NAME, "locations-feedback") # Tries to find the "not found" element
                    print(Console.RED + "No results  " + Console.RESET)
                    return {
                        "address": address,
                        "url": None
                    }
                except:
                    try:
                        driver.find_element(By.CSS_SELECTOR, 'a[class="multiselect__redirect"]') # Tries to find the first element of "Imobiliárias"
                        print(Console.RED + "No results  " + Console.RESET)
                        return {
                            "address": address,
                            "url": None
                        }
                    except:
                        print("Searching...", end="\r")

        location_div.click()

        sleep(1)

        street_url = driver.current_url
        print(Console.GREEN + "Success: " + Console.RESET + f"{street_url}")

        location_div.click()
        
        return {
            "address": address,
            "url": street_url
        }
    else:
        print(Console.BLUE + "Skipped " + Console.RESET + f"{address}")

def fix_unwanted_urls(driver: webdriver):
    print("Looking for mistakes...")
    result = database.query(
        "SELECT id, address FROM zapimoveis.address_urls WHERE url NOT LIKE '%%https://www.zapimoveis.com.br/venda/imoveis/rj%%'"
        )
    if result:
        for item in result:
            address = item[1]
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
                    db_functions.Zapimoveis.update_address_url(database, address_url)
    else:
        print("All good!")

@timed
def __main__():

    global database

    driver = webdriver.Chrome()

    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    driver.get("https://www.zapimoveis.com.br/venda/?itl_id=1000063&itl_name=zap_-_link-header_comprar_to_zap_resultado-pesquisa")

    fix_unwanted_urls(driver)

    cities = db_functions.get_all_cities(database)
    for city in cities:
        locations = db_functions.get_locations_from_city(database, city["city_name"], "RJ")

        for index, location in enumerate(locations):
            print(Console.BLACK + f"{index + 1}/{len(locations)}" + Console.RESET, end=" ")
            address_url = get_address_url(driver, location)
            if address_url:
                db_functions.Zapimoveis.insert_address_url(database, address_url)
        
        # fix_unwanted_urls(driver)
        


    driver.quit()

if __name__ == "__main__":
    __main__()
import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))
# Resolve module imports

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from unidecode import unidecode

from time import sleep
from threading import Thread

from utils.wrappers import timed
from utils.functions import error
from database.connection import Database
from database.functions.zapimoveis import *
from database.functions.public import *
from utils.constants import ConsoleColors as Console
from utils.wrappers import announce_off

announce_off()

database = Database(ensure_connection=True)

cities = []
stored_addresses = []

main_url = "https://www.zapimoveis.com.br/venda/?__ab=exp-aa-test:control,rec-cta:rcta,desc-phone:pcta&transacao=venda&pagina=1"
default_urls = [
    main_url,
    "https://www.zapimoveis.com.br/venda/?__ab=exp-aa-test:control,novopos:new,rp-imob:enabled,rec-cta:rcta,desc-phone:pcta&transacao=venda&pagina=1"
]

def check_address_similarity(local_address: str, web_address: str) -> bool:
    # format: STREET, CITY - STATE

    # handling edgecase
    web_address = web_address.replace(", S/No", "")

    local_street, local_city_state = local_address.split(", ")
    web_street, web_city_state = web_address.split(", ")
    if local_city_state == web_city_state:
        for word in local_street.split(" "):
            if word not in web_street:
                return False
        return True
    else:
        return False

def location_to_address(location: dict):
    address = f"{location['street']}, {location['city']} - {location['state']}"
    address = address.replace("'", "")
    return address

def get_address_url(driver: webdriver.Chrome, location: dict, update = False) -> dict:

    global database
    global main_url
    global default_urls
    
    address = location_to_address(location)

    try:

        if not check_address_url_exists(database, {"address": address, "url": None}) or update:

            print(Console.BOLD_WHITE + f"Getting url from address: {address}" + Console.RESET)

            # finds the search bar
            while True:
                try:
                    text_input = Wait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Digite o nome da rua, bairro ou cidade"]')))
                    print(text_input.text)
                    text_input.click()
                    break
                except Exception as e:
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

            # types the address
            while True:
                try:
                    driver.execute_script(f"arguments[0].value = '{address}';", text_input)
                    text_input.send_keys(Keys.SPACE)
                    break
                except Exception as e:
                    print(f"Error: {e}\nTrying again...")

            # handles the result
            while True:
                try:
                    location_div = Wait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-cy="locations-item-input"]'))) # Tries to find the address selection element
                    if not check_address_similarity(address, unidecode(location_div.text.upper())):
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
            sleep(1)

            while driver.current_url in default_urls:
                # print(driver.current_url, default_urls)
                sleep(0.1)

            street_url = driver.current_url
            # last_gathered_url = street_url

            clear_button = Wait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "search-multiselect__clean-button")))
            clear_button.click()

            clear_inputs()

            print(Console.GREEN + "Success: " + Console.RESET + f"{street_url}")

            return {
                "address": address,
                "url": street_url
            }
        else:
            print(Console.BLUE + "Skipped " + Console.RESET + f"{address}")
    except Exception as e:
        error(e)

def fix_mistakes():
    global main_url
    global database

    result = database.query(
        "SELECT address FROM zapimoveis.address_urls WHERE url NOT LIKE '%%https://www.zapimoveis.com.br/venda/imoveis/%%'"
    )
    if result:
        options = webdriver.ChromeOptions()
        options.add_argument('--log-level=3')

        driver = webdriver.Chrome(options=options)

        driver.get(main_url)

        print("Fixing mistakes...")
        for index, item in enumerate(result):
            print(f"{index + 1}/{len(result)}", end=" ")
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
        print("Done!")
        driver.quit()

def link_scraper(x: int, y: int):
    global cities
    global stored_addresses
    global main_url

    database = Database(ensure_connection=True)

    options = webdriver.ChromeOptions()
    options.add_argument('--log-level=3')

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(900, 900)
    driver.set_window_position(x + 30, y + 30)

    driver.get(main_url)

    while len(cities) > 0:
        city = cities[0]
        cities.pop(0)

        state = get_state_by_id(database, city["city_state"])
        locations = get_locations_from_city(database, city["city_name"], state["state_acronym"])

        aux = locations[:]
        for item in aux:
            if location_to_address(item) in stored_addresses:
                locations.remove(item)

        for index, location in enumerate(locations):
            print(Console.BLACK + f"{index + 1}/{len(locations)}" + Console.RESET, end=" ")
            address_url = get_address_url(driver, location)
            if address_url:
                insert_address_url(database, address_url)

    driver.quit()

@timed
def __main__():

    global main_url
    global cities
    global stored_addresses

    fix_mistakes()

    cities = get_all_cities(database)
    stored_addresses = [item["address"] for item in get_address_urls(database)]
                    
    thread_list = []
    for i in range(10):
        thread = Thread(target=link_scraper, args=(100 * i, 0))
        thread.start()
        thread_list.append(thread)
        sleep(10)
    
    for thread in thread_list:
        thread.join()

if __name__ == "__main__":
    __main__()
import os
import sys

current_file = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file)
project_root = os.path.dirname(current_directory)
sys.path.append(project_root)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth
from selenium.webdriver.common.keys import Keys

from time import sleep
import json
import signal
import atexit

from utils.constants import ConsoleColors as Console
from utils.functions import create_dirs

OUTPUT_PATH = r"output/location_data"
OUTPUT_FILE_PATH = OUTPUT_PATH + r"/street_urls.json"
LOCATIONS_FILE_PATH = OUTPUT_PATH + r"/locations.json"

street_urls = list()
stored_url_addresses = list()

def wait(driver, sec):
    return WebDriverWait(driver, sec)

def get_street_url(driver: webdriver.Chrome, location: dict):
    global stored_url_addresses
    
    address = f"{location['street']}, {location['city']} - {location['state']}"

    if address not in stored_url_addresses:
        print(f"Getting url from address: {address}")

        text_input = wait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Digite o nome da rua, bairro ou cidade"]')))

        text_input.click()
        while True:
            try:
                sleep(1)
                driver.execute_script(f"arguments[0].value = '{address}';", text_input)
                text_input.send_keys(Keys.SPACE)
                break
            except Exception as e:
                print(f"Error: {e}\nTrying again...")
                append_urls_to_json(street_urls)

        while True:
            try:
                location_div = wait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-cy="locations-item-input"]')))
                break
            except:
                try:
                    driver.find_element(By.CLASS_NAME, "locations-feedback") # Tries to find the "not found" element
                    print(Console.RED + "Invalid address" + Console.RESET)
                    return {
                        "street": address,
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
            "street": address,
            "url": street_url
        }
    else:
        print(Console.BLUE + "Skipped " + Console.RESET + f"{address}")

def append_urls_to_json():
    global street_urls
    print("Storing urls...", end=" ")
    create_dirs(OUTPUT_FILE_PATH)
    with open(OUTPUT_FILE_PATH, "w") as json_file:
        json.dump({"street_urls": street_urls}, json_file, indent=4, ensure_ascii=False)
    print(Console.GREEN + "Done" + Console.RESET)

def get_stored_address_urls():
    try:
        stored_url_addresses: list = list()
        with open(OUTPUT_FILE_PATH, "r") as json_file:
            temp = json.load(json_file)["street_urls"]
            for item in temp:
                stored_url_addresses.append(item["street"])
            return stored_url_addresses
    except:
        print("No urls stored")
        return []

# Signal handling function for termination signals (such as SIGINT, SIGTERM)
def signal_handler(sig, frame):
    print("\nTerminating")
    append_urls_to_json()
    sys.exit(0)

def __main__():

    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C

    global street_urls
    global stored_url_addresses

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

    with open(LOCATIONS_FILE_PATH, "r") as json_file:
        locations = json.load(json_file)["locations"]
    
    stored_url_addresses = get_stored_address_urls()
    for location in locations:
        url = get_street_url(driver, location)
        if url:
            street_urls.append(url)

    append_urls_to_json()

    driver.quit()

if __name__ == "__main__":
    __main__()
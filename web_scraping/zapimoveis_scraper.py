import os
import sys
import json
import threading
from time import time, sleep
import traceback
import signal

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth

from realty_scraper import scrape_realty
from utils.constants import ConsoleColors as console
from utils.functions import *

REALTY_DIV_SIZE = 300
REALTIES_PER_PAGE = 100
OUTPUT_PATH = r"output/"
REALTIES_JSON = OUTPUT_PATH + r"realty_data/realties.json"
SCRAPED_REALTY_URLS_JSON = OUTPUT_PATH + r"scraped_urls/scraped_realty_urls.json"
SCRAPED_STREET_URLS_JSON = OUTPUT_PATH + r"scraped_urls/scraped_street_urls.json"
STREET_URLS_JSON = OUTPUT_PATH + r"location_data/street_urls.json"

pause_loading = False
scraped_realties = 0
total_realties = 1

# Signal handling function for termination signals (such as SIGINT, SIGTERM)
def signal_handler(sig, frame):
    print("Termination signal detected:", sig)
    append_to_realties_json("realties", scrape_url())
    sys.exit(0)

pause_loading = False

def load_realties(driver: webdriver.Chrome, realty_list_div: WebElement):
    global pause_loading
    global total_realties
    global scraped_realties
    STEP = 100
    while True:
        loaded_realties = len(realty_list_div.find_elements(By.CLASS_NAME, "l-card__wrapper"))
        if loaded_realties >= REALTIES_PER_PAGE:
            break  
        elif loaded_realties >= (total_realties - scraped_realties): # In case it's the last page
            break

        driver.execute_script(f"window.scrollBy(0, {STEP});")

        # Reset scrolling if needed
        max_y = loaded_realties * REALTY_DIV_SIZE
        current_scroll_y = driver.execute_script("return window.scrollY;")
        if current_scroll_y >= max_y:
            driver.execute_script(f"window.scrollTo(0, {max_y * 0.2});")
        sleep(0.001)

        while pause_loading:
            sleep(0.3)

def append_to_realties_json(obj_name, new_list):
    print("Saving realties...", end=" ")
    create_dirs(REALTIES_JSON)
    current_list: list = list()
    try:
        with open(REALTIES_JSON, "r") as json_file:
            current_list = json.load(json_file)["realties"]
        for item in new_list:
            if item not in current_list:
                current_list.append(item)
    except:
        pass
    with open(REALTIES_JSON, "w") as json_file:
        json.dump({f"{obj_name}": current_list}, json_file, indent=4, ensure_ascii=False)
    print(console.GREEN + "Done" + console.RESET)
    print_log(f"json saved with {len(current_list)} realties")

def get_scraped_realty_urls():
    try:
        with open(SCRAPED_REALTY_URLS_JSON) as json_file:
            url_dict = json.load(json_file)
        return url_dict["urls"]
    except:
        print(f"File not found: {SCRAPED_REALTY_URLS_JSON}")
        return []

def append_to_scraped_streets(url):
    print("Saving scraped street urls...", end=" ")
    create_dirs(SCRAPED_STREET_URLS_JSON)
    url_list: list = list()
    try:
        with open(SCRAPED_STREET_URLS_JSON, "r") as json_file:
            url_list = json.load(json_file)["scraped_street_urls"]
            if url not in url_list:
                url_list.append(url)
    except:
        pass
    with open(SCRAPED_STREET_URLS_JSON, "w") as json_file:
        json.dump({"scraped_street_urls": url_list}, json_file, indent=4, ensure_ascii=False)
    print(console.GREEN + "Done" + console.RESET)
    print_log(f"json saved with {len(url_list)} urls")

def get_scraped_street_urls():
    try:
        with open(SCRAPED_STREET_URLS_JSON, "r") as json_file:
            return json.load(json_file)["scraped_street_urls"]
    except:
        print(f"File not found: {SCRAPED_STREET_URLS_JSON}")
        return []

def get_street_urls():
    try:
        with open(STREET_URLS_JSON, "r") as json_file:
            return json.load(json_file)["street_urls"]
    except:
        print(f"File not found: {STREET_URLS_JSON}")
        return []

def scrape_url(url: str):
    url = url[:-1] # Remove the page index

    global scraped_realties
    global total_realties
    global pause_loading
    stored_urls = get_scraped_realty_urls()
    all_realties = list()
    current_page = 1
    while scraped_realties < total_realties:
        try:
            print(console.BLUE + f"PAGE {current_page}" + console.RESET)

            driver = webdriver.Chrome()

            stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
            )
            
            driver.get(url + f"{current_page}")
            wait = WebDriverWait(driver, 10)

            try:
                total_realties_h1 = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "h1.l-text.l-u-color-neutral-12.l-text--variant-heading-small.l-text--weight-semibold.undefined"))
                )
            except:
                print("Connection error")
                continue
            total_realties = int(total_realties_h1.text.split(" ")[0].replace(".", ""))

            realty_list_div = driver.find_element(By.CLASS_NAME, "listing-wrapper")

            loader = threading.Thread(target=load_realties, args=(driver, realty_list_div))
            loader.start()

            data_position = 1
            while data_position <= REALTIES_PER_PAGE and scraped_realties < total_realties:

                try:
                    realty_div = driver.find_element(By.CSS_SELECTOR, f'div[data-position="{data_position}"]')
                    try:
                        # Extract the URL of the realty
                        realty_a = realty_div.find_element(By.TAG_NAME, "a")
                        url = realty_a.get_attribute("href")
                    except NoSuchElementException:
                        # Handle special case when link is not directly available
                        pause_loading = True
                        show_all_button = realty_div.find_element(By.XPATH, ".//*[contains(text(), 'Exibir Anúncios')]")
                        show_all_button.click()
                        sleep(1.5)
                        duplicate_list_div = driver.find_element(By.CLASS_NAME, "deduplication-listings__listings")
                        duplicate_a_tags = duplicate_list_div.find_elements(By.TAG_NAME, "a")
                        url = duplicate_a_tags[0].get_attribute("href")
                        close_span = driver.find_element(By.CSS_SELECTOR, f'span[aria-label="Fechar modal lateral"]')
                        close_span.click()
                        pause_loading = False
                    finally:
                        if url not in stored_urls:
                            print(f"Scraping realty number {data_position}")
                            try:
                                # Scrape realty info
                                start_time = time()
                                realty_info = scrape_realty(url)
                                execution_time = time() - start_time
                                print(f"Realty scraped in {format_time(execution_time)}")
                            except Exception as e:
                                # Handle scraping errors
                                realty_info = None
                                print(console.RED + f"Error at webpage: {url}" + console.RESET)
                                traceback.print_exc()
                                append_to_realties_json("realties", all_realties)
                            if realty_info != None:
                                all_realties.append(realty_info)
                        data_position += 1
                        scraped_realties += 1
                except NoSuchElementException:
                    print("Loading...", end="\r")
                except Exception as e:
                    print(f"Error: {e}")

            loader.join()
            driver.quit()
            current_page += 1
            if current_page > 100:
                break
        except Exception as e:
            print(f"ERROR: {e}")
            append_to_realties_json("realties", all_realties)
            break

    return all_realties

def __main__():

    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Termination command

    start_time = time()

    global pause_loading
    global scraped_realties
    global total_realties

    all_realties = list()

    street_urls = get_street_urls()
    for street in street_urls:
        print(f"Scraping realties from: {street['street']}")

        # Reset global variables
        pause_loading = False
        scraped_realties = 0
        total_realties = 1

        all_realties = scrape_url(street["url"])

        append_to_scraped_streets(street["url"])
    append_to_realties_json("realties", all_realties)

    execution_time = time() - start_time
    print(f"Total execution done in {format_time(execution_time)}")
    print("Remeber to turn your sleep timer back on")


if __name__ == "__main__":
    __main__()
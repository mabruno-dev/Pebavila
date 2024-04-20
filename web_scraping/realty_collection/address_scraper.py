import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))
# Resolve module imports

import random
import threading
import json
from time import sleep, time
import inspect

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

from utils.functions import error, create_dirs
from utils.wrappers import timed, announce_off
from web_scraping.realty_collection.realty_scraper import scrape_realty
from database.connection import Database
from database.functions.public import *
from database.functions.zapimoveis import *
from database.functions.sctracker import *
from utils.constants import ConsoleColors as Console

realty_div_size = 300 # Usually 300 but may vary
REALTIES_PER_PAGE = 100

scraped_realties = 0
total_realties = 1

pause_loading = False
stop_loading = False

scraper_running = True
realty_list = []

announce_off()

class InvalidStatusKeyException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def load_realties(driver: webdriver.Chrome, realty_list_div: WebElement):

    global realty_div_size
    global pause_loading
    global stop_loading
    global total_realties
    global scraped_realties

    loaded_realties = 0
    stop_loading = False

    while not stop_loading and loaded_realties < total_realties:
        loaded_realties = len(realty_list_div.find_elements(By.CLASS_NAME, "l-card__wrapper"))

        driver.execute_script(f"window.scrollBy(0, {realty_div_size / 3});")

        # Reset scrolling if needed
        max_y = (loaded_realties + 5) * realty_div_size
        current_scroll_y = driver.execute_script("return window.scrollY;")
        if current_scroll_y >= max_y:
            driver.execute_script(f"window.scrollTo(0, {max_y * 0.15});")
        sleep(0.001)
        while pause_loading and not stop_loading:
            sleep(0.3)

    stop_loading = False

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

def scrape_realties(x: int, y: int):
    global scraper_running
    global realty_list
    
    database = Database()

    driver = uc.Chrome(options=set_driver_options())
    driver.set_window_size(450, 450)
    driver.set_window_position(x, y)

    MIN_TIME = 5

    while scraper_running:
        if len(realty_list) > 0:
            item = realty_list[0]
            realty_list.pop(0)
            if "end" in item.keys():
                set_address_url_scraped(database, item["end"])
            else:
                start_time = time()
                if item["realty"]:
                    if not check_realty_exists_by_url(database, item["realty"]):
                        print(Console.YELLOW + "Scraping" + Console.RESET + f" realty {item["index"]} from {item["address"]}")
                        try:
                            set_status(database, current_realty_start=time(), current_realty_image=item["image"])
                            realty_info = scrape_realty(driver, item["realty"])
                        except TypeError as e:
                            realty_info = None
                            print(Console.RED + f"{e}" + Console.RESET)
                        except NoSuchElementException as e:
                            realty_info = None
                            print(Console.RED + f"{e}" + Console.RESET)
                        except Exception as e:
                            realty_info = None
                            print(Console.RED + f"Error at webpage: {item["realty"]}" + Console.RESET)
                            continue
                        if realty_info != None:
                            insert_realty(database, realty_info)
                    else:
                        print(Console.BLUE + "Skipped"  + Console.RESET + f" realty {item["index"]} from {item["address"]}")

                    delta_time = time() - start_time
                    if delta_time < MIN_TIME:
                        sleep(MIN_TIME - delta_time)
            
        else:
            sleep(3)

@timed
def scrape_address(database: Database, driver: webdriver, address_url: dict):
    url = address_url["url"][:-1] # Remove the page index
    
    global realty_list
    global realty_div_size
    global pause_loading
    global stop_loading
    global total_realties

    total_realties = 1
    collected_realty_urls = 0
    current_page = 1

    while collected_realty_urls < total_realties and current_page <= 100:
        start_time = time()
        try:
            page_url = url + f"{current_page}"
            driver.get(page_url)
            wait = WebDriverWait(driver, 10)

            driver.get(page_url)

            try:
                # verify_human(driver)
                total_realties_h1 = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "h1.l-text.l-u-color-neutral-12.l-text--variant-heading-small.l-text--weight-semibold.undefined"))
                )
            except:
                print(Console.RED + "Connection error" + Console.RESET)
                break
            try:
                total_realties = int(total_realties_h1.text.split(" ")[0].replace(".", ""))
            except:
                print("No realties in this url")
                current_page = 101
                continue

            realty_list_div = driver.find_element(By.CLASS_NAME, "listing-wrapper")

            loader = threading.Thread(target=load_realties, args=(driver, realty_list_div))
            loader.start()
            loading_time = 0

            data_position = 1

            while data_position <= REALTIES_PER_PAGE and collected_realty_urls < total_realties:
                try:
                    realty_div = driver.find_element(By.CSS_SELECTOR, f'div[data-position="{data_position}"]')
                    realty_div_size = realty_div.size["height"]

                    image = realty_div.find_element(By.TAG_NAME, "img")
                    image_url = image.get_attribute("src")

                    try:
                        # Extract the URL of the realty
                        realty_a = realty_div.find_element(By.TAG_NAME, "a")
                        realty_url = realty_a.get_attribute("href")
                    except NoSuchElementException:
                        # Handle special case when link is not directly available
                        # pause_loading = True
                        # show_all_button = realty_div.find_element(By.XPATH, ".//*[contains(text(), 'Exibir Anúncios')]")
                        # show_all_button.click()
                        # sleep(1.5)
                        # duplicate_list_div = driver.find_element(By.CLASS_NAME, "deduplication-listings__listings")
                        # duplicate_a_tags = duplicate_list_div.find_elements(By.TAG_NAME, "a")
                        # realty_url = duplicate_a_tags[0].get_attribute("href")
                        # close_span = driver.find_element(By.CSS_SELECTOR, f'span[aria-label="Fechar modal lateral"]')
                        # close_span.click()
                        # pause_loading = False
                        realty_url = None # for now
                    finally:
                        realty_list.append({
                            "index": data_position,
                            "realty": realty_url,
                            "image": image_url,
                            "address": address_url["address"]
                        })
                        data_position += 1
                        collected_realty_urls += 1
                except NoSuchElementException:
                    pause_loading = False

                    loading_time = time() - start_time
                    if loading_time > 90:
                        print("Loading took too long, reloading page")
                        current_page = 101
                        break
                    
                except Exception as e:
                    # set_status(database, error=str(e))
                    # error(e)
                    pass

            stop_loading = True
            loader.join()
            current_page += 1
        except Exception as e:
            set_status(database, error=str(e))
            error(e)

    realty_list.append({"end": address_url})

def reset_control_variables():

    global pause_loading
    global scraped_realties
    global total_realties

    pause_loading = False
    scraped_realties = 0
    total_realties = 1


@timed
def __main__():

    database = Database()
    
    global scraper_running
    global realty_list

    driver = uc.Chrome(options=set_driver_options())
    driver.set_window_size(600, 600)
    driver.set_window_position(15, 15)

    set_status(database, scraper_start=time(), running=True)

    address_url_list = get_address_urls(database)
    random.shuffle(address_url_list) # This is done so that multiple instances of the scraper have less chance of scraping the same url at the same time
    
    realty_scrapers = []
    for i in range(10):

        thread = threading.Thread(target=scrape_realties, args=(15 * (i + 2), 15 * (i + 2)))
        thread.start()
        realty_scrapers.append(thread)

    for address_url in address_url_list:
        if address_url["url"] != None:
            if not check_address_url_is_scraped(database, address_url["address"]):
                print(Console.YELLOW + "Scraping" + Console.RESET + f" realties from: {address_url['address']}")

                set_status(database, address=address_url["address"])

                reset_control_variables()
                scrape_address(database, driver, address_url)
            else:
                print(Console.BLUE + "Skipped" + Console.RESET + f" address: {address_url['address']}")
    
    while len(realty_list) > 0:
        sleep(15)
    scraper_running = False

if __name__ == "__main__":
    __main__()

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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

from utils.functions import error, create_dirs
from utils.wrappers import timed
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

database = Database(ensure_connection=True)

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
    STEP = 100

    while not stop_loading and loaded_realties < total_realties:
        loaded_realties = len(realty_list_div.find_elements(By.CLASS_NAME, "l-card__wrapper"))

        driver.execute_script(f"window.scrollBy(0, {STEP});")

        # Reset scrolling if needed
        max_y = loaded_realties * realty_div_size
        current_scroll_y = driver.execute_script("return window.scrollY;")
        if current_scroll_y >= max_y:
            driver.execute_script(f"window.scrollTo(0, {max_y * 0.15});")
        sleep(0.001)

        while pause_loading and not stop_loading:
            sleep(0.3)

    stop_loading = False

def scrape_realties(driver: webdriver, realty_list: list, address_url: dict):
    global database
    try:
        for index, item in enumerate(realty_list):
            if not check_realty_exists_by_url(database, item["realty"]):
                print(Console.YELLOW + "Scraping" + Console.RESET + f" realty number {index + 1}")
                try:
                    set_status(database, current_realty_start=time(), current_realty_image=item["image"])
                    # Scrape realty info
                    realty_info = scrape_realty(driver, item["realty"])
                except Exception as e:
                    # Handle scraping errors
                    realty_info = None
                    print(Console.RED + f"Error at webpage: {item["realty"]}" + Console.RESET)
                if realty_info != None:
                    insert_realty(database, realty_info)
            else:
                print(Console.BLUE + "Skipped"  + Console.RESET + f" realty number {index + 1}")
        set_address_url_scraped(database, address_url)
    except Exception as e:
        error(e)

@timed
def scrape_url(driver: webdriver, address_url: dict):
    url = address_url["url"][:-1] # Remove the page index
    
    global database
    global realty_div_size
    global pause_loading
    global stop_loading

    total_realties = 1
    realty_list = []
    current_page = 1

    while len(realty_list) < total_realties and current_page <= 100:
        start_time = time()
        try:
            page_url = url + f"{current_page}"
            driver.get(page_url)
            wait = WebDriverWait(driver, 10)

            driver.get(page_url)

            try:
                total_realties_h1 = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "h1.l-text.l-u-color-neutral-12.l-text--variant-heading-small.l-text--weight-semibold.undefined"))
                )
            except:
                print(Console.RED + "Connection error" + Console.RESET)
                break
            total_realties = int(total_realties_h1.text.split(" ")[0].replace(".", ""))

            realty_list_div = driver.find_element(By.CLASS_NAME, "listing-wrapper")

            loader = threading.Thread(target=load_realties, args=(driver, realty_list_div))
            loader.start()
            loading_time = 0

            data_position = 1

            while data_position <= REALTIES_PER_PAGE and len(realty_list) < total_realties:
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
                        pause_loading = True
                        show_all_button = realty_div.find_element(By.XPATH, ".//*[contains(text(), 'Exibir Anúncios')]")
                        show_all_button.click()
                        sleep(1.5)
                        duplicate_list_div = driver.find_element(By.CLASS_NAME, "deduplication-listings__listings")
                        duplicate_a_tags = duplicate_list_div.find_elements(By.TAG_NAME, "a")
                        realty_url = duplicate_a_tags[0].get_attribute("href")
                        close_span = driver.find_element(By.CSS_SELECTOR, f'span[aria-label="Fechar modal lateral"]')
                        close_span.click()
                        pause_loading = False
                    finally:
                        realty_list.append({
                            "realty": realty_url,
                            "image": image_url
                        })
                        data_position += 1
                except NoSuchElementException:
                    pause_loading = False

                    loading_time = time() - start_time
                    if loading_time > 120:
                        print("Loading took too long, reloading page")
                        current_page -= 1
                        break

                    print(f"Loading...", end="\r")
                    
                    if not loader.is_alive():
                        loader = threading.Thread(target=load_realties, args=(driver, realty_list_div))
                        loader.start()
                except Exception as e:
                    set_status(database, error=str(e))
                    error(e)

            stop_loading = True
            loader.join()
            current_page += 1
        except Exception as e:
            set_status(database, error=str(e))
            error(e)

    scrape_realties(driver, realty_list, address_url)

def reset_control_variables():

    global pause_loading
    global scraped_realties
    global total_realties

    pause_loading = False
    scraped_realties = 0
    total_realties = 1

@timed
def __main__():

    global database
    global end_script

    driver = uc.Chrome()

    set_status(database, scraper_start=time(), running=True)

    address_url_list = get_address_urls(database)
    random.shuffle(address_url_list) # This is done so that multiple instances of the scraper have less chance of scraping the same url at the same time

    for address_url in address_url_list:
        if address_url["url"] != None:
            if not check_address_url_is_scraped(database, address_url["address"]):
                print(Console.YELLOW + "Scraping" + Console.RESET + f" realties from: {address_url['address']}")

                set_status(database, address=address_url["address"])

                reset_control_variables()
                scrape_url(driver, address_url)
            else:
                print(Console.BLUE + "Skipped" + Console.RESET + f" address: {address_url['address']}")

if __name__ == "__main__":
    __main__()

import os
import json
import threading
from time import time, sleep
import traceback

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from realty_scraper import scrape_realty
from utils.constants import ConsoleColors as console
from utils.functions import format_time

REALTY_DIV_SIZE = 300
REALTIES_PER_PAGE = 100
BASE_URL = "https://www.zapimoveis.com.br/venda/imoveis/rj+niteroi/?__ab=seo-texts:control,exp-aa-test:B&transacao=venda&onde=,Rio%20de%20Janeiro,Niterói,,,,,city,BR%3ERio%20de%20Janeiro%3ENULL%3ENiteroi,-22.823378,-43.04625,&pagina="

pause_loading = False  # Global variable to control loading pause


def load_realties(driver: webdriver.Chrome, realty_list_div: WebElement):
    global pause_loading
    STEP = 100
    while True:
        loaded_realties = len(realty_list_div.find_elements(By.CLASS_NAME, "l-card__wrapper"))
        if loaded_realties == REALTIES_PER_PAGE:
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


def scrape_website():
    global pause_loading
    all_realties = list()
    current_page = 1
    scraped_realties = 0
    total_realties = 1
    while scraped_realties <= total_realties:

        print(console.BLUE + f"PAGE {current_page}" + console.RESET)

        driver = webdriver.Chrome()
        driver.get(BASE_URL + f"{current_page}")
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
        while data_position <= REALTIES_PER_PAGE:

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
                    duplicate_list_div = wait.until(
                        EC.presence_of_element_located((By.CLASS_NAME, "deduplication-listings__listings"))
                    )
                    duplicate_a_tags = duplicate_list_div.find_elements(By.TAG_NAME, "a")
                    url = duplicate_a_tags[0].get_attribute("href")
                    close_span = driver.find_element(By.CSS_SELECTOR, f'span[aria-label="Fechar modal lateral"]')
                    close_span.click()
                    pause_loading = False
                finally:
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

    return all_realties


def __main__():
    start_time = time()

    all_realties = scrape_website()

    # Write scraped realties to a JSON file
    json_object = {"realties": all_realties}
    OUTPUT_PATH = r"realty_collection/output"
    os.makedirs(OUTPUT_PATH)
    with open(OUTPUT_PATH + f"/realties.json", "w") as json_file:
        json.dump(json_object, json_file, indent=4, ensure_ascii=False)

    execution_time = time() - start_time
    print(f"Total execution done in {format_time(execution_time)}")
    print("Remeber to turn your sleep timer back on")


if __name__ == "__main__":
    __main__()

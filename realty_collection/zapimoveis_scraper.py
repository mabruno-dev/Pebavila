from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from time import sleep
import threading
from realty_scraper import scrap_realty

REALTY_DIV_SIZE = 300
REALTIES_PER_PAGE = 100
BASE_URL = "https://www.zapimoveis.com.br/venda/imoveis/rj+niteroi/?__ab=seo-texts:control,exp-aa-test:B&transacao=venda&onde=,Rio%20de%20Janeiro,Niterói,,,,,city,BR%3ERio%20de%20Janeiro%3ENULL%3ENiteroi,-22.823378,-43.04625,&pagina="

def load_realties(driver: webdriver.Chrome, realty_list_div: WebElement):
    STEP = 100
    while True:
        loaded_realties = len(realty_list_div.find_elements(By.CLASS_NAME, "l-card__wrapper"))
        if loaded_realties == REALTIES_PER_PAGE:
            break

        driver.execute_script(f"window.scrollBy(0, {STEP});")

        max_y = loaded_realties * 300
        current_scroll_y = driver.execute_script("return window.scrollY;")
        if current_scroll_y == max_y:
            driver.execute_script(f"window.scrollTo(0, {max_y * 0.2});")
        sleep(0.001)

def scrape_website():
    current_page = 1
    scrapped_realties = 0
    total_realties = 1
    while scrapped_realties < total_realties:

        print(f"\nPÁGINA {current_page}")

        driver = webdriver.Chrome()
        driver.get(BASE_URL + f"{current_page}")
        sleep(3)

        total_realties_h1 = driver.find_element(By.CSS_SELECTOR, "h1.l-text.l-u-color-neutral-12.l-text--variant-heading-small.l-text--weight-semibold.undefined")
        total_realties = int(total_realties_h1.text.split(" ")[0].replace(".", ""))

        realty_list_div = driver.find_element(By.CLASS_NAME, "listing-wrapper")

        loader = threading.Thread(target=load_realties, args=(driver, realty_list_div))
        loader.start()

        data_position = 1
        while(data_position <= REALTIES_PER_PAGE):

            try:
                realty_div = driver.find_element(By.CSS_SELECTOR, f'div[data-position="{data_position}"]')
                try:
                    print(f"Scrapping realty number {data_position}")
                    realty_a = realty_div.find_element(By.TAG_NAME, "a")
                    url = realty_a.get_attribute("href")
                    print(scrap_realty(url))
                except:
                    print("Skipped (unsolved edge case)")
                    show_all_button = realty_div.find_element(By.CSS_SELECTOR, 'button[data-testid="l-button"]')
                finally:
                    data_position += 1
                    scrapped_realties += 1
            except:
                print("Loading...", end="\r")

        loader.join()
        driver.quit()
        current_page += 1

def __main__():
    scrape_website()

if __name__ == "__main__":
    __main__()

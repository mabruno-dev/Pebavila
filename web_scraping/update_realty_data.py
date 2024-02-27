import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))
# Resolve module imports

from database.connection import Database
from database.functions import *
from web_scraping.realty_scraper import scrape_realty

from time import time, sleep
import random

database = Database(ensure_connection=True, persistent=True)

def __main__():
    realty_urls = get_outdated_realty_urls(database)
    random.shuffle(realty_urls)
    for url in realty_urls:
        start_time = time()
        realty = scrape_realty(url)
        update_realty_by_url(database, realty)
        while time() - start_time < 5:
            sleep(1)

if __name__ == "__main__":
    __main__()
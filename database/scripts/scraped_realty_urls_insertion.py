import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))
# Resolve module imports

import json
from database.functions import Zapimoveis
from database.connection import Database

def __main__():
    with open(r"output/location_data/scraped_street_urls.json") as json_file:
        list = json.load(json_file)["street_urls"]
        for item in list:
            item["address"] = item["street"]
            Zapimoveis.insert_address_url(Database(), item)

if __name__ == "__main__":
    __main__()
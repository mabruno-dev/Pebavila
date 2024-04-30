import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))
# Resolve module imports

from database.connection import Database
from database.functions.public import insert_street_neighborhood_city
import json

database = Database(ensure_connection=True)

def __main__():
    file_path = 'output/addresses.json'
    with open(file_path, 'r') as file:
        addresses = json.load(file)
    for key1 in addresses.keys():
        for key2 in addresses[key1].keys():
            for key3 in addresses[key1][key2].keys():
                for item in addresses[key1][key2][key3]:
                    location = {
                        "state": key1,
                        "city": key2,
                        "neighborhood": key3,
                        "street": item
                    }
                    insert_street_neighborhood_city(database, location)


if __name__ == "__main__":
    __main__()
import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))
# Resolve module imports

from database.functions.public import set_streets_neighborhoods_cities
import json

def __main__():
    file_path = 'output/addresses.json'
    with open(file_path, 'r') as file:
        streets = json.load(file)

    set_streets_neighborhoods_cities(streets)

if __name__ == "__main__":
    __main__()
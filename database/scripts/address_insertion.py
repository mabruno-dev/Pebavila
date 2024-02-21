import os
import sys

current_file = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file)
project_root = os.path.dirname(current_directory)
sys.path.append(project_root)

from database.db_functions import set_streets_neighborhoods_cities
import json

def __main__():
    file_path = 'C:/Users/matbr/OneDrive/Área de Trabalho/Projetos/the-beginning/address_collection/output/addresses.json'
    with open(file_path, 'r') as file:
        streets = json.load(file)

    set_streets_neighborhoods_cities(streets)

if __name__ == "__main__":
    __main__()
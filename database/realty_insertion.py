import json
from db_functions import insert_realties

REALTIES_JSON_PATH = r"output/realty_data/realties.json"

def __main__():
    with open(REALTIES_JSON_PATH) as json_file:
        realties = json.load(json_file)
    insert_realties(realties)

if __name__ == "__main__":
    __main__()
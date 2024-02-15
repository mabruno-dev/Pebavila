import json
from db_functions import insert_realties

REALTIES_JSON_PATH = r"output/realty_data/realties.json"

def __main__():
    try:
        with open(REALTIES_JSON_PATH) as json_file:
            realties = json.load(json_file)
        print(realties)
        insert_realties(realties)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    __main__()
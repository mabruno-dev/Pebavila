import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))
# Resolve module imports

import json
from database.functions import insert_realties

REALTIES_JSON_PATH = r"output/realty_data/realties.json"

def __main__():
    try:
        with open(REALTIES_JSON_PATH) as json_file:
            realties = json.load(json_file)
        insert_realties(realties)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    __main__()
from database.db_functions import get_locations_from_city

import json
import os

OUTPUT_PATH = r"output/location_data"
OUTPUT_FILE = OUTPUT_PATH + r"/locations.json"

def __main__():
    locations = get_locations_from_city("niteroi", "rj")
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    with open(OUTPUT_FILE, "w") as json_file:
        json.dump({"locations": locations}, json_file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    __main__()
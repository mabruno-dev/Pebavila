import os
import sys

current_file = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file)
project_root = os.path.dirname(current_directory)
sys.path.append(project_root)

from database.db_functions import get_realty_urls
import json

OUTPUT_FILE = r"output/realty_data/realty_urls.json"

def __main__():
    url_list = get_realty_urls()
    with open(OUTPUT_FILE, "w") as json_file:
        json.dump({"realty_urls": url_list}, json_file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    __main__()
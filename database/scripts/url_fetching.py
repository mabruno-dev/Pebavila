import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))
# Resolve module imports

from database.functions.public import get_realty_urls
import json

OUTPUT_FILE = r"output/realty_data/realty_urls.json"

def __main__():
    url_list = get_realty_urls()
    with open(OUTPUT_FILE, "w") as json_file:
        json.dump({"realty_urls": url_list}, json_file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    __main__()
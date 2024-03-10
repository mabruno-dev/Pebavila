import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))
# Resolve module imports

from database.connection import Database
from utils.functions import print_log

def __main__():
    database = Database(ensure_connection=True)

    result = database.queryone(
        "SELECT COUNT(*) FROM public.realties"
    )
    total_realties = result[0]

    result = database.queryone('''
        SELECT
            (SELECT COUNT(*) FROM zapimoveis.address_urls WHERE scraped = 1),
            (SELECT COUNT(*) FROM zapimoveis.address_urls WHERE scraped = 0 AND url IS NOT NULL)
    ''')
    scraped_urls = result[0]
    not_scraped_urls = result[1]
    
    print_log(f"TOTAL REALTIES: {total_realties}", showDt=True)
    print_log(f"SCRAPED URLS: {scraped_urls} | NOT SCRAPED URLS: {not_scraped_urls}", showDt=True)

    print_log("-" * 40, onConsole=False)

if __name__ == "__main__":
    __main__()
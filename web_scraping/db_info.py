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

    last_address_url = database.queryone(
        "SELECT address FROM zapimoveis.address_urls ORDER BY id DESC LIMIT 1"
    )[0]

    result = database.queryone('''
        SELECT 
            s1.street_name,
            n.neighborhood_name,
            c.city_name,
            s2.state_acronym
        FROM
            public.realties AS r
        INNER JOIN public.neighborhoods n ON r.realty_neighborhood = n.neighborhood_id
        INNER JOIN public.streets s1 ON r.realty_street = s1.street_id
        INNER JOIN public.cities c ON n.neighborhood_city = c.city_id
        INNER JOIN public.states s2 ON c.city_state = state_id
        ORDER BY realty_id DESC LIMIT 1
        '''
    )
    last_realty_address = f"{result[0]}, {result[1]} - {result[2]} ({result[3]})"
    
    print_log(f"TOTAL REALTIES: {total_realties}")
    print_log(f"LAST STORED REALTY ADDRESS: {last_realty_address}")

    print_log(f"SCRAPED URLS: {scraped_urls} | NOT SCRAPED URLS: {not_scraped_urls}")
    print_log(f"LAST URL STORED: {last_address_url}", showDt=True, section=True)


if __name__ == "__main__":
    __main__()
import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))
# Resolve module imports

from utils.wrappers import announce
from utils.constants import ConsoleColors as Console
from database.connection import Database

from datetime import datetime

class QueryFormatingException(Exception):
    pass

class InvalidLocationException(Exception):
    pass

def error(database: Database, e: Exception):
    database.connection.rollback() # Allow the connection to continue operating
    print(f"{Console.RED} {e}{Console.RESET}")

@announce
def generic_delete(schema_name, table_name, id_record):
    try:
        with Database() as database:
            database.execute("UPDATE %s.%s SET active = 0, updated_at = %s WHERE state_id = %s", (
                          schema_name, table_name, datetime.now(), id_record))
            database.commit()
        return "success"
    except Exception as e:
        error(database, e)

@announce
def generic_update():
    try:
        pass
    except Exception as e:
        # error(database, e)
        pass

@announce
def get_state_id(database: Database, state_acronym: str):
    state_acronym = state_acronym.upper()
    try:
        state_id = database.queryone(
            'SELECT state_id FROM public.states WHERE state_acronym = %s', (state_acronym,))
        if state_id:
            return state_id[0]

    except Exception as e:
        error(database, e)

@announce
def get_or_insert_city(database: Database, city_name, state_id):
    try:
        city_id = database.queryone(
            'SELECT city_id FROM public.cities WHERE city_name = %s', (city_name,))

        if city_id:
            return city_id[0]
        else:
            database.execute(
                'INSERT INTO public.cities (city_name, city_state) VALUES(%s, %s) RETURNING city_id', (city_name, state_id))
            city_id = database.fetchone()[0]
            database.commit()
            print("Record added to the database succesfully")
            return city_id
    except Exception as e:
        error(database, e)

@announce
def get_or_insert_neighborhood(database: Database, neighborhood_name, city_id):
    try:
        neighborhood_id = database.queryone(
            "SELECT neighborhood_id FROM public.neighborhoods WHERE neighborhood_name = %s",
            (neighborhood_name,)
        )

        if neighborhood_id:
            return neighborhood_id[0]
        else:
            database.execute(
                'INSERT INTO public.neighborhoods (neighborhood_name, neighborhood_city) VALUES (%s, %s) RETURNING neighborhood_id',
                (neighborhood_name, city_id)
            )

            neighborhood_id = database.fetchone()[0]
            database.commit()
            print("Record added to the database succesfully")
            return neighborhood_id
    except Exception as e:
        error(database, e)

@announce
def check_street_exists(database: Database, street_name, neighborhood_id):
    try:
        street_id = database.queryone(
            'SELECT street_id FROM public.streets WHERE street_name = %s AND street_neighborhood = %s',
            (street_name, neighborhood_id)
        )

        return street_id is not None
    except Exception as e:
        error(database, e)
    try:
        database.execute(
            'INSERT INTO public.streets (street_name, street_neighborhood) VALUES (%s, %s)',
            (street_name, neighborhood_id)
        )
        database.commit()
    except Exception as e:
        error(database, e)

@announce
def check_neighborhood_exists(database: Database, neighborhood_name, city_id):
    try:
        neighborhood_id = database.queryone(
            'SELECT neighborhood_id FROM public.neighborhoods WHERE neighborhood_name = %s AND neighborhood_city = %s',
            (neighborhood_name, city_id)
        )

        return neighborhood_id is not None
    except Exception as e:
        error(database, e)
    try:
        database.execute(
            'INSERT INTO public.neighborhoods (neighborhood_name, neighborhood_city) VALUES (%s, %s)',
            (neighborhood_name, city_id)
        )
        database.commit()
    except Exception as e:
        error(database, e)

@announce
def insert_street(database: Database, street_name: str, neighborhood_id: int):
    try:
        if not check_street_exists(database, street_name, neighborhood_id):
            database.execute(
                "INSERT INTO public.streets (street_name, street_neighborhood) VALUES (%s, %s)",
                (street_name, neighborhood_id)
            )
            database.commit()
            print("Record added to database succesfully")
        else:
            print("Record already exists")
    except Exception as e:
        error(database, e)

@announce
def insert_street_neighborhood_city(database: Database, location: dict):
    try:
        state_id = get_state_id(database, location['state'])
        city_id = get_or_insert_city(database, location['city'], state_id)
        neighborhood_id = get_or_insert_neighborhood(
            database, location['neighborhood'], city_id)

        if neighborhood_id is not None:
            street_exists = check_street_exists(
                database, location['street'], neighborhood_id)

            if street_exists:
                print('Record already exists')
            else:
                database.execute(
                    'INSERT INTO public.streets (street_name, street_neighborhood) VALUES(%s, %s)', 
                    (location['street'], neighborhood_id)
                )
                database.commit()
                print('Record added to the database successfully')
    except Exception as e:
        error(database, e)

@announce
def insert_neighborhood_city(database: Database, location: dict):
    try:
        state_id = get_state_id(database, location['state'])
        city_id = get_or_insert_city(database, location['city'], state_id)
        if city_id is not None:
            neighborhood_exists = check_neighborhood_exists(
                database, location['neighborhood'], city_id)

            if neighborhood_exists:
                print('Record already exists')
            else:
                database.execute(
                    'INSERT INTO public.neighborhoods (neighborhood_name, neighborhood_city) VALUES(%s, %s)', 
                    (location['neighborhood'], city_id)
                )
                database.commit()
                print('Record added to the database successfully')
    except Exception as e:
        error(database, e)

@announce
def set_streets_neighborhoods_cities(json_streets):
    try:
        with Database() as database:
            for street in json_streets['addresses']:
                insert_street_neighborhood_city(database, street)
    except Exception as e:
        error(database, e)

@announce
def get_street_id(database: Database, street_name: str, neighborhood_id):
    try:
        street_name = street_name.upper()
        street_id = database.queryone(
            "SELECT street_id FROM public.streets WHERE street_name = %s AND street_neighborhood = %s",
            (street_name, neighborhood_id)
        )
        if street_id:
            return street_id[0]
        else:
            pass
    except Exception as e:
        error(database, e)

@announce
def get_neighborhood_id(database: Database, neighborhood_name: str, city_id):
    try:
        neighborhood_name = neighborhood_name.upper()
        neighborhood_id = database.queryone(
            "SELECT neighborhood_id FROM public.neighborhoods WHERE neighborhood_name = %s AND neighborhood_city = %s",
            (neighborhood_name, city_id)
        )
        if neighborhood_id:
            return neighborhood_id[0]
    except Exception as e:
        database.connection.rollback() # Allow the connection to continue operating    
        print(f"Error: {e}")

@announce
def get_city_id(database: Database, city_name: str, state_id):
    try:
        city_name = city_name.upper()
        city_id = database.queryone(
            "SELECT city_id FROM public.cities WHERE city_name = %s AND city_state = %s",
            (city_name, state_id)
        )
        if city_id:
            return city_id[0]
    except Exception as e:
        database.connection.rollback() # Allow the connection to continue operating 
        print(f"Error: {e}")

def get_realty_street(database: Database, location):
    # returns the foreign key for street
    state_id = get_state_id(database, location["state"])
    city_id = get_city_id(database, location["city"], state_id)
    neighborhood_id = get_neighborhood_id(database, location["neighborhood"], city_id)
    street_id = get_street_id(database, location["street"], neighborhood_id)
    if street_id:
        return street_id

def get_realty_neighborhood(database: Database, location):
    # returns the foreign key for neighborhood
    state_id = get_state_id(database, location["state"])
    city_id = get_city_id(database, location["city"], state_id)
    neighborhood_id = get_neighborhood_id(database, location["neighborhood"], city_id)
    if neighborhood_id:
        return neighborhood_id

@announce
def get_realty_advertiser(database: Database, advertiser: str):
    # returns the foreign key for advertiser
    try:
        advertiser = advertiser.upper()
        advertiser_id = database.queryone(
            "SELECT advertiser_id FROM public.advertisers WHERE advertiser_name = %s", (advertiser,)
        )
        if advertiser_id:
            return advertiser_id[0]
    except Exception as e:
        database.connection.rollback() # Allow the connection to continue operating       
        print(f"Error: {e}")

@announce
def insert_advertiser(database: Database, advertiser: str):
    try:
        if not database.queryone(
            "SELECT advertiser_id FROM public.advertisers WHERE advertiser_name = %s", (advertiser,)
        ):
            database.execute(
                "INSERT INTO public.advertisers (advertiser_name) values (%s)", (advertiser,)
            )
            database.commit()
            print("Record added to the database successfully")
        else:
            print("Record already exists")
    except Exception as e:
        database.connection.rollback() # Allow the connection to continue operating
        print(f"Error {e}")

@announce
def get_realty_type(database: Database, type: str):
    # returns the foreign key for advertiser
    try:
        type = type.upper()
        type_id = database.queryone(
            "SELECT type_id FROM public.types WHERE type_name = %s", (type,)
        )
        if type_id:
            return type_id[0]
    except Exception as e:
        database.connection.rollback() # Allow the connection to continue operating  
        print(f"Error: {e}")

@announce
def insert_type(database: Database, type: str):
    try:
        if not database.queryone(
            "SELECT type_id FROM public.types WHERE type_name = %s", (type,)
        ):
            database.execute(
                "INSERT INTO public.types (type_name) values (%s)", (type,)
            )
            database.commit()
            print("Record added to the database successfully")
        else:
            print("Record already exists")
    except Exception as e:
        database.connection.rollback() # Allow the connection to continue operating
        print(f"Error {e}")

def comparison_query(string: str, values: tuple):
    # String must have 2x more %s's than the number of values.
    # This function handles the presence of null values, 
    # adapting it to a select query with comparison in PostgreSQL
    if string.count("%s") / 2 == len(values):
        temp = list()
        for value in values:
            if value is None:
                temp.append("IS")
                temp.append("NULL")
            else:
                temp.append("=")
                temp.append(f"'{value}'")
        string_values = tuple(temp)
        return string % string_values
    else:
        raise QueryFormatingException("Mismatch between number of values and %s's")

@announce
def get_all_cities(database: Database):
    try:
        result = database.query(
            "SELECT * FROM public.cities"
        )
        cities = [{
            "city_id": item[0],
            "city_name": item[1],
            "city_state": item[2]
            } for item in result]
        return cities
    except Exception as e:
        database.connection.rollback() # Allow the connection to continue operating
        print(f"Error {e}")

@announce
def get_all_neighborhoods(database: Database):
    try:
        result = database.query(
            "SELECT * FROM public.neighborhoods"
        )
        neighborhoods = [{
            "neighborhood_id": item[0],
            "neighborhood_name": item[1],
            "neighborhood_city": item[2]
            } for item in result]
        return neighborhoods
    except Exception as e:
        database.connection.rollback() # Allow the connection to continue operating
        print(f"Error {e}")

@announce
def get_all_streets(database: Database):
    try:
        result = database.query(
            "SELECT * FROM public.streets"
        )
        streets = [{
            "street_id": item[0],
            "street_name": item[1],
            "street_neighborhood": item[2]
            } for item in result]
        return streets
    except Exception as e:
        database.connection.rollback() # Allow the connection to continue operating
        print(f"Error {e}")

@announce
def validate_location(database: Database, location: dict):
    valid_location = dict()

    # Validate state
    state_id = get_state_id(database, location["state"])
    if state_id:
        valid_location["state"] = location["state"]
    else:
        raise InvalidLocationException("State does not exist")

    # Validate city
    city_id = get_city_id(database, location["city"], state_id)
    if city_id:
        valid_location["city"] = location["city"]
    else:
        raise InvalidLocationException("City does not exist")
    
    # Validate neighborhood
    neighborhood_id = get_neighborhood_id(database, location["neighborhood"], city_id)
    if neighborhood_id:
        valid_location["neighborhood"] = location["neighborhood"]
    else:
        # Check if neighborhood exists in the database
        neighborhood_list = get_all_neighborhoods(database)
        if neighborhood_list:
            # Attempt to find a match
            for item in neighborhood_list:
                if item["neighborhood_name"].replace(" ", "") == location["neighborhood"].replace(" ", ""):
                    if item["neighborhood_city"] == city_id:
                        valid_location["neighborhood"] = item["neighborhood_name"]
                        break
        # If not found, insert it
        if not "neighborhood" in valid_location:
            neighborhood_id = get_or_insert_neighborhood(database, location["neighborhood"], city_id)
            valid_location["neighborhood"] = location["neighborhood"]

    # Validate street if provided
    if location["street"] is not None:
        street_id = get_street_id(database, location["street"], neighborhood_id)
        if street_id:
            valid_location["street"] = location["street"]
        else:
            # Check if street exists in the database
            street_list = get_all_streets(database)
            if street_list:
                # Attempt to find a match
                for item in street_list:
                    if item["street_name"].replace(" ", "") == location["street"].replace(" ", ""):
                        if item["street_neighborhood"] == neighborhood_id:
                            valid_location["street"] = item["street_name"]
                            break
            # If not found, insert it
            if not "street" in valid_location:
                insert_street(database, location["street"], neighborhood_id)
                valid_location["street"] = location["street"]
    else:
        valid_location["street"] = None

    return valid_location

@announce
def normalize_realty_dict(database: Database, realty: dict):
    if not "realty_location" in realty:
        return realty
    
    normalized_realty = realty.copy()
    # get neighborhood FK
    neighborhood = get_realty_neighborhood(database, realty["realty_location"])
    if not neighborhood:
        raise InvalidLocationException("Neighborhood does not exist")
    else:
        normalized_realty["realty_neighborhood"] = neighborhood

    # get street FK
    if realty["realty_location"]["street"] is not None:
        street = get_realty_street(database, realty["realty_location"])
        if not street:
            raise InvalidLocationException("Street does not exist")
        else:
            normalized_realty["realty_street"] = street
    else:
        normalized_realty["realty_street"] = None

    del normalized_realty["realty_location"]

    # get type FK    
    type = get_realty_type(database, realty["realty_type"])
    if not type:
        insert_type(database, realty["realty_type"])
        type = get_realty_type(database, realty["realty_type"])
    normalized_realty["realty_type"] = type

    # get advertiser FK
    advertiser = get_realty_advertiser(database, realty["realty_advertiser"])
    if not advertiser:
        insert_advertiser(database, realty["realty_advertiser"])
        advertiser = get_realty_advertiser(database, realty["realty_advertiser"])
    normalized_realty["realty_advertiser"] = advertiser

    return normalized_realty


@announce
def check_realty_exists(database: Database, realty: dict):
    try:
        realty = normalize_realty_dict(database, realty)
        return database.queryone(
            comparison_query('''
                SELECT realty_id 
                FROM public.realties 
                WHERE realty_neighborhood %s %s
                AND realty_street %s %s
                AND realty_number %s %s
                AND realty_square_footage %s %s 
                AND realty_floor %s %s 
                AND realty_price %s %s
                ''',
                (realty["realty_neighborhood"], realty["realty_street"], realty["realty_number"], realty["realty_square_footage"], realty["realty_floor"], realty["realty_price"])
            )
        )
    except Exception as e:
        error(database, e)

@announce
def insert_realty(database: Database, realty: dict):
    try:
        realty["realty_location"] = validate_location(database, realty["realty_location"])
        realty = normalize_realty_dict(database, realty)
        if realty:
            if not check_realty_exists(database, realty):
                columns = list(realty.keys())
                values = list(realty.values())
                placeholders = ', '.join(['%s'] * len(columns))
                database.execute(
                    f"INSERT INTO public.realties ({', '.join(columns)}) VALUES ({placeholders})",
                    values
                )
                database.commit()
                print("Record added to the database successfully")
            else:
                print("Record already exists")
    except Exception as e:
        error(database, e)

# @announce
# def update_realty_by_url(database: Database, realty: dict):
#     try:
#         realty = normalize_realty_dict(database, realty)
#         result = database.queryone(
#             "SELECT realty_id, up_to_date FROM public.realties WHERE realty_url = %s",
#             (realty["realty_url"],)
#         )
#         print(result)
#         realty_id = result[0]
#         up_to_date = result[1]
#         if realty_id: 
#             if not up_to_date:
#                 assignments = list()
#                 for key, value in realty.items():
#                     if value == None:
#                         assignments.append(f"{key} = NULL")
#                     elif isinstance(value, str):
#                         temp = value.replace("'", "''")
#                         assignments.append(f"{key} = '{temp}'")
#                     else:
#                         assignments.append(f"{key} = {value}")
#                 updates = ", ".join(assignments)
#                 database.execute(
#                     f"UPDATE public.realties SET {updates}, up_to_date = 1, updated_at = %s WHERE realty_id = %s",
#                     (datetime.now(), realty_id)
#                 )
#                 database.commit()
#                 print("Record successfuly updated")
#             else:
#                 print("Record is up to date")
#         else:
#             print("Record not found")
#     except Exception as e:
#         database.connection.rollback()
#         print(f"Error: {e}")

@announce
def get_neighborhood_name(database: Database, neighborhood_id):
    try:
        data = database.queryone(
            "SELECT * FROM public.neighborhoods WHERE neighborhood_id = %s", 
            (neighborhood_id,)
        )
        return data[1]
    except Exception as e:
        error(database, e)

@announce
def get_locations_from_city(database: Database, city: str, state: str):
    try:
        locations = list()
        state_id = get_state_id(database, state)
        city_id = get_city_id(database, city, state_id)

        result = database.query('''
            SELECT 
                street.street_name,
                neighborhood.neighborhood_name,
                city.city_name,
                state.state_acronym
            FROM 
                public.streets AS street
            INNER JOIN public.neighborhoods neighborhood ON street.street_neighborhood = neighborhood.neighborhood_id
            INNER JOIN public.cities city ON neighborhood.neighborhood_city = city.city_id
            INNER JOIN public.states state ON city.city_state = state.state_id
            WHERE city.city_id = %s;
            ''',
            (city_id,)
        )
        for item in result:
            location = {
                "street": item[0],
                "neighborhood": item[1],
                "city": item[2],
                "state": item[3]
            }
            locations.append(location)
        return locations
    except Exception as e:
        error(database, e)

@announce
def get_realty_urls(database: Database):
    try:
        url_list = list()
        temp = database.query("SELECT realty_url FROM public.realties")
        for item in temp:
            url_list.append(item[0])
        return url_list
    except Exception as e:
        error(database, e)

@announce
def check_realty_exists_by_url(database: Database, url: str):
    try:
        return database.query(
            "SELECT realty_id FROM public.realties WHERE realty_url = %s",
            (url,)
        )
    except Exception as e:
        error(database, e)

@announce
def check_address_url_exists(database: Database, address_url: dict):
    try:
        return database.queryone(
            "SELECT id FROM address_urls WHERE address = %s", 
            (address_url["address"],)
        )
    except Exception as e:
        database.connection.rollback() # Allow the connection to continue operating
        print(f"Error: {e}")
        
@announce
def insert_address_url(database: Database, address_url: dict):
    try:
        if not check_address_url_exists(database, address_url):
            database.execute(
                "INSERT INTO address_urls (address, url) VALUES (%s, %s)", 
                (address_url["address"], address_url["url"])
            )
            database.commit()
            print("Record added to the database successfully")
        else:
            print("Record already exists")
    except Exception as e:
        database.connection.rollback() # Allow the connection to continue operating
        print(f"Error: {e}")

@announce
def update_address_url(database: Database, address_url: dict):
    try:
        if check_address_url_exists(database, address_url):
            database.execute(
                "UPDATE address_urls SET url = %s, updated_at = %s WHERE address = %s",
                (address_url["url"], datetime.now(), address_url["address"])
            )
            database.commit()
            print("Record updated successfully")
    except Exception as e:
        database.connection.rollback() # Allow the connection to continue operating
        print(f"Error: {e}")

@announce
def get_address_urls(database: Database):
    try:
        result = database.query(
            "SELECT * FROM address_urls"
        )
        address_url_list = list()
        for item in result:
            address_url = {
                "address": item[1],
                "url": item[2]
            }
            address_url_list.append(address_url)
        return address_url_list
    except Exception as e:
        database.connection.rollback()
        print(f"Error: {e}")

@announce
def set_address_url_scraped(database: Database, address_url: dict):
    try:
        database.execute(
            "UPDATE address_urls SET scraped = 1 WHERE address = %s",
            (address_url["address"],)
        )
        database.commit()
    except Exception as e:
        database.connection.rollback()
        print(f"Error: {e}")

@announce
def set_address_url_not_scraped(database: Database, address_url: dict):
    try:
        database.execute(
            "UPDATE address_urls SET scraped = 0 WHERE address = %s",
            (address_url["address"],)
        )
        database.commit()
    except Exception as e:
        database.connection.rollback()
        print(f"Error: {e}")

@announce
def check_address_url_is_scraped(database: Database, address: str):
        try:
            result = database.queryone(
                "SELECT scraped FROM address_urls WHERE address = %s",
                (address,)
            )
            return result[0]
        except Exception as e:
            database.connection.rollback()
            print(f"Error: {e}")





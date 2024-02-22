import os
import sys

current_file = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file)
project_root = os.path.dirname(current_directory)
sys.path.append(project_root)

from db_connection import Database
from utils.constants import ConsoleColors as console

from datetime import datetime

class QueryFormatingException(Exception):
    pass

def generic_delete(schema_name, table_name, id_record):
    try:
        with Database() as database:
            database.execute("UPDATE %s.%s SET active = 0, updated_at = %s WHERE state_id = %s", (
                          schema_name, table_name, datetime.now(), id_record))
            database.commit()
        return "success"
    except Exception as E:
        print(E)

def generic_update():
    try:
        pass
    except Exception as E:
        print(E)

def get_state_id(database: Database, state_acronym: str):
    state_acronym = state_acronym.upper()
    try:
        state_id = database.queryone(
            'SELECT state_id FROM public.states WHERE state_acronym = %s', (state_acronym,))
        if state_id:
            return state_id[0]

    except Exception as E:
        print(E)

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
            return city_id
    except Exception as E:
        print(E)

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
            return neighborhood_id
    except Exception as E:
        print(E)

def check_street_exists(database: Database, street_name, neighborhood_id):
    try:
        street_id = database.queryone(
            'SELECT street_id FROM public.streets WHERE street_name = %s AND street_neighborhood = %s',
            (street_name, neighborhood_id)
        )

        return street_id is not None
    except Exception as E:
        print(E)
    try:
        database.execute(
            'INSERT INTO public.streets (street_name, street_neighborhood) VALUES (%s, %s)',
            (street_name, neighborhood_id)
        )
        database.commit()
    except Exception as E:
        print(E)

def set_streets_neighborhoods_cities(json_streets):
    try:
        with Database() as database:
            for street in json_streets['addresses']:
                state_id = get_state_id(database, street['state'])
                city_id = get_or_insert_city(database, street['city'], state_id)
                neighborhood_id = get_or_insert_neighborhood(
                    database, street['neighborhood'], city_id)

                if neighborhood_id is not None:
                    street_exists = check_street_exists(
                        database, street['street'], neighborhood_id)

                    if street_exists:
                        print('Record already exists')
                    else:
                        database.execute('INSERT INTO public.streets (street_name, street_neighborhood) VALUES(%s, %s)', (
                            street['street'], neighborhood_id))
                        database.commit()
                        print('Record added to the database successfully')

    except Exception as e:
        print(f"Error: {e}")

def get_street_id(database: Database, street_name: str, neighborhood_id):
    street_name = street_name.upper()
    try:
        street_id = database.queryone(
            "SELECT street_id FROM public.streets WHERE street_name = %s AND street_neighborhood = %s",
            (street_name, neighborhood_id)
        )
        if street_id:
            return street_id[0]
    except Exception as e:
        print(f"Error: {e}")

def get_neighborhood_id(database: Database, neighborhood_name: str, city_id):
    neighborhood_name = neighborhood_name.upper()
    try:
        neighborhood_id = database.queryone(
            "SELECT neighborhood_id FROM public.neighborhoods WHERE neighborhood_name = %s AND neighborhood_city = %s",
            (neighborhood_name, city_id)
        )
        if neighborhood_id:
            return neighborhood_id[0]
    except Exception as e:
        print(f"Error: {e}")

def get_city_id(database: Database, city_name: str, state_id):
    city_name = city_name.upper()
    try:
        city_id = database.queryone(
            "SELECT city_id FROM public.cities WHERE city_name = %s AND city_state = %s",
            (city_name, state_id)
        )
        if city_id:
            return city_id[0]
    except Exception as e:
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
    
def get_realty_advertiser(database: Database, advertiser: str):
    # returns the foreign key for advertiser
    advertiser = advertiser.upper()
    try:
        advertiser_id = database.queryone(
            "SELECT advertiser_id FROM public.advertisers WHERE advertiser_name = %s", (advertiser,)
        )
        if advertiser_id:
            return advertiser_id[0]
    except Exception as e:
        print(f"Error: {e}")

def insert_advertiser(database: Database, advertiser: str):
    try:
        if not database.queryone(
            "SELECT advertiser_id FROM public.advertisers WHERE advertiser_name = %s", (advertiser,)
        ):
            database.execute(
                "INSERT INTO public.advertisers (advertiser_name) values (%s)", (advertiser,)
            )
            database.commit()
            print("New advertiser inserted")
        else:
            print("Advertiser already exists")
    except Exception as e:
        print(f"Error {e}")

def get_realty_type(database: Database, type: str):
    # returns the foreign key for advertiser
    type = type.upper()
    try:
        type_id = database.queryone(
            "SELECT type_id FROM public.types WHERE type_name = %s", (type,)
        )
        if type_id:
            return type_id[0]
    except Exception as e:
        print(f"Error: {e}")

def insert_type(database: Database, type: str):
    try:
        if not database.queryone(
            "SELECT type_id FROM public.types WHERE type_name = %s", (type,)
        ):
            database.execute(
                "INSERT INTO public.types (type_name) values (%s)", (type,)
            )
            database.commit()
            print("New type inserted")
        else:
            print("Type already exists")
    except Exception as e:
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

def insert_realties(realties_dict):
    with Database() as database:
        for realty in realties_dict["realties"]:
            realty = dict(realty)

            # get neighborhood FK
            neighborhood = get_realty_neighborhood(database, realty["realty_location"])
            if not neighborhood:
                print("Location does not exist")
                continue
            else:
                realty["realty_neighborhood"] = neighborhood

            # get street FK
            if realty["realty_location"]["street"] is not None:
                street = get_realty_street(database, realty["realty_location"])
                if not street:
                    print("Location does not exist")
                    continue
                else:
                    realty["realty_street"] = street
            else:
                realty["realty_street"] = None

            del realty["realty_location"]

            # get type FK    
            type = get_realty_type(database, realty["realty_type"])
            if not type:
                insert_type(database, realty["realty_type"])
                type = get_realty_type(database, realty["realty_type"])
            realty["realty_type"] = type

            # get advertiser FK
            advertiser = get_realty_advertiser(database, realty["realty_advertiser"])
            if not advertiser:
                insert_advertiser(database, realty["realty_advertiser"])
                advertiser = get_realty_advertiser(database, realty["realty_advertiser"])
            realty["realty_advertiser"] = advertiser

            if not database.queryone(
                comparison_query('''
                    SELECT realty_id 
                    FROM public.realties 
                    WHERE realty_street %s %s 
                    AND realty_number %s %s
                    AND realty_square_footage %s %s 
                    AND realty_floor %s %s 
                    AND realty_price %s %s
                    ''',
                    (realty["realty_street"], realty["realty_number"], realty["realty_square_footage"], realty["realty_floor"], realty["realty_price"])
                )):
                columns = list(realty.keys())
                values = list(realty.values())
                placeholders = ', '.join(['%s'] * len(columns))
                try:
                    database.execute(
                        f"INSERT INTO public.realties ({', '.join(columns)}) VALUES ({placeholders})",
                        values
                    )
                    database.commit()
                    print("Succesfully inserted")
                except Exception as e:
                    database.connection.rollback() # allow the function to continue inserting realties
                    print(f"Error inserting realty: {e}")
            else:
                print("Record already exists")

def get_neighborhood_name(database: Database, neighborhood_id):
    try:
        data = database.queryone(
            "SELECT * FROM public.neighborhoods WHERE neighborhood_id = %s", 
            (neighborhood_id,)
        )
        return data[1]
    except Exception as e:
        print(f"Error: {e}")

def get_locations_from_city(city: str, state: str):
    locations = list()
    with Database() as database:
        state_id = get_state_id(database, state)
        city_id = get_city_id(database, city, state_id)

        neighborhood_id_list = database.query(
            "SELECT neighborhood_id FROM public.neighborhoods WHERE neighborhood_city = %s", 
            (city_id,)
        )

        for neighborhood_id in neighborhood_id_list:
            neighborhood_id = neighborhood_id[0]
            street_list = database.query(
                "SELECT street_name FROM public.streets WHERE street_neighborhood = %s", 
                (neighborhood_id,)
            )

            for street in street_list:
                street = street[0]
                location_dict = {
                    "state": state.upper(),
                    "city": city.upper(),
                    "neighborhood": get_neighborhood_name(database, neighborhood_id),
                    "street": street
                }
                locations.append(location_dict)

    return locations

def get_realty_urls():
    with Database() as database:
        url_list = list()
        temp = database.query("SELECT realty_url FROM public.realties")
        for item in temp:
            url_list.append(item[0])
        print(url_list)
        return url_list

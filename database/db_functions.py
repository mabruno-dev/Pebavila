from db_connection import Database
from datetime import datetime
# from models.states import Set_state
import json
# import models


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
        
# def add_states(jsonStates: models.states.Set_state):
#     try:
#         with Database() as database:
#             for state in jsonStates.states:
#                 result = database.queryone(
#                     "SELECT state_id FROM public.states WHERE state_name = %s AND state_acronym = %s", (state.state_name, state.state_acronym))
#                 if result:
#                     pass
#                 else:
#                     database.execute("INSERT INTO public.states (state_name, state_acronym) VALUES(%s,%s)", (
#                         state.state_name.upper(), state.state_acronym.upper()))
#                     database.commit()
#         return print("Success")
#     except Exception as E:
#         print(E)


# states = models.states.Set_state(states=[
#     {"state_name": "Acre", "state_acronym": "AC"},
#     {"state_name": "Alagoas", "state_acronym": "AL"},
#     {"state_name": "Amapa", "state_acronym": "AP"},
#     {"state_name": "Amazonas", "state_acronym": "AM"},
#     {"state_name": "Bahia", "state_acronym": "BA"},
#     {"state_name": "Ceara", "state_acronym": "CE"},
#     {"state_name": "Distrito Federal", "state_acronym": "DF"},
#     {"state_name": "Espirito Santo", "state_acronym": "ES"},
#     {"state_name": "Goias", "state_acronym": "GO"},
#     {"state_name": "Maranhao", "state_acronym": "MA"},
#     {"state_name": "Mato Grosso", "state_acronym": "MT"},
#     {"state_name": "Mato Grosso do Sul", "state_acronym": "MS"},
#     {"state_name": "Minas Gerais", "state_acronym": "MG"},
#     {"state_name": "Para", "state_acronym": "PA"},
#     {"state_name": "Paraiba", "state_acronym": "PB"},
#     {"state_name": "Parana", "state_acronym": "PR"},
#     {"state_name": "Pernambuco", "state_acronym": "PE"},
#     {"state_name": "Piaui", "state_acronym": "PI"},
#     {"state_name": "Rio de Janeiro", "state_acronym": "RJ"},
#     {"state_name": "Rio Grande do Norte", "state_acronym": "RN"},
#     {"state_name": "Rio Grande do Sul", "state_acronym": "RS"},
#     {"state_name": "Rondonia", "state_acronym": "RO"},
#     {"state_name": "Roraima", "state_acronym": "RR"},
#     {"state_name": "Santa Catarina", "state_acronym": "SC"},
#     {"state_name": "Sao Paulo", "state_acronym": "SP"},
#     {"state_name": "Sergipe", "state_acronym": "SE"},
#     {"state_name": "Tocantins", "state_acronym": "TO"}
# ])


def get_state_id(database: Database, state_acronym):
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

def get_street_id(database: Database, street_name, neighborhood_id):
    try:
        street_id = database.queryone(
            "SELECT street_id FROM public.streets WHERE street_name = %s AND street_neighborhood = %s",
            (street_name, neighborhood_id)
        )
        if street_id:
            return street_id[0]
    except Exception as e:
        print(f"Error: {e}")

def get_neighborhood_id(database: Database, neighborhood_name, city_id):
    try:
        neighborhood_id = database.queryone(
            "SELECT neighborhood_id FROM public.neighborhoods WHERE neighborhood_name = %s AND neighborhood_city = %s",
            (neighborhood_name, city_id)
        )
        if neighborhood_id:
            return neighborhood_id[0]
    except Exception as e:
        print(f"Error: {e}")

def get_city_id(database: Database, city_name, state_id):
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
    state_id = get_state_id(database, location["state"])
    city_id = get_city_id(database, location["city"], state_id)
    neighborhood_id = get_neighborhood_id(database, location["neighborhood"], city_id)
    street_id = get_street_id(database, location["street"], neighborhood_id)
    if street_id:
        return street_id


def insert_realties(realties_dict):
    with Database() as database:
        for realty in realties_dict["realties"]:
            realty = dict(realty)
            street = get_realty_street(database, realty["realty_location"])
            if not street:
                set_streets_neighborhoods_cities({"addresses": [realty["realty_location"]]})
                street = get_realty_street(database, realty["realty_location"])
            del realty["realty_location"]
            realty["realty_street"] = street

            aux = realty.copy()
            for key, value in aux.items():
                if value == None:
                    del realty[f"{key}"]
            print(realty)

            if not database.queryone('''
                SELECT realty_id 
                FROM public.realties 
                WHERE realty_street = %s 
                AND realty_number = %s 
                AND realty_square_footage = %s 
                AND realty_floor = %s 
                AND realty_price = %s
                ''',
                (realty["realty_street"], realty["realty_number"], realty["realty_square_footage"], realty["realty_floor"], realty["realty_price"])
            ):
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
                    print(f"Error inserting realty: {e}")
            else:
                print("Record already exists")

insert_realties({
    "realties": [{
        "realty_number": "137",
        "realty_location": {
            "state": "RJ",
            "city": "NITEROI",
            "neighborhood": "ICARAI",
            "street": "RUA DOUTOR PAULO CESAR"
        },
        "realty_square_footage": 150,
        "realty_price": 5435435,
        "realty_description": "BEAUTIFUL HOUSE WITH A SPACIOUS BACKYARD AND MODERN AMENITIES.",
        "realty_parking_spaces": 2,
        "realty_bathrooms": 2,
        "realty_bedrooms": 3,
        "realty_advertiser": "SPIN",
        "realty_advertiser_number": "555-123-4567",
        "realty_done": 1,
        "realty_property_tax": 2500.00,
        "realty_furnished": "1",
        "realty_condo_price": 3000.00,
        "realty_floor": 2,
        "realty_type": "APARTMENT",
        "realty_url": "www.sexosexosexosexo.com"
    },
    {
        "realty_number": "137",
        "realty_location": {
            "state": "RJ",
            "city": "NITEROI",
            "neighborhood": "SAO FRANCISCO",
            "street": "AVENIDA QUINTINO BOCAIUVA"
        },
        "realty_square_footage": 150,
        "realty_price": 5435435,
        "realty_description": "BEAUTIFUL HOUSE WITH A SPACIOUS BACKYARD AND MODERN AMENITIES.",
        "realty_parking_spaces": 2,
        "realty_bathrooms": 2,
        "realty_bedrooms": 1,
        "realty_advertiser": "SPIN",
        "realty_advertiser_number": "555-123-4567",
        "realty_done": 2,
        "realty_property_tax": 2500.00,
        "realty_furnished": "1",
        "realty_condo_price": 3000.00,
        "realty_floor": 2,
        "realty_type": "APARTMENT",
        "realty_url": "www.sexosexosexosexo.com"
    },
    {
        "realty_location": {
            "state": "SP",
            "city": "SAO JOSE DO RIO PRETO",
            "neighborhood": "PARQUE INDUSTRIAL",
            "street": "RUA PEDRO AMARAL"
        },
        "realty_number": 2496,
        "realty_square_footage": 137,
        "realty_price": 320000.0,
        "realty_description": "kjasdkjhasd",
        "realty_parking_spaces": None,
        "realty_bathrooms": 3,
        "realty_bedrooms": 3,
        "realty_advertiser": "ROMA PRIME NEGOCIOS IMOBILIARIOS",
        "realty_advertiser_number": "375908",
        "realty_done": 2,
        "realty_property_tax": None,
        "realty_furnished": "0",
        "realty_condo_price": None,
        "realty_floor": 4,
        "realty_type": "APARTAMENTO",
        "realty_url": "https://www.zapimoveis.com.br/imovel/venda-apartamento-3-quartos-com-zelador-parque-industrial-sao-jose-do-rio-preto-sp-137m2-id-2580372921/"
    }]
})



            
            

            

            
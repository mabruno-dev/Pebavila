from db_connection import Database
from datetime import datetime
import models
import json

def generic_delete(schema_name, table_name, id_record):
    try:
        with Database() as banco:
            banco.execute("UPDATE %s.%s SET active = 0, updated_at = %s WHERE state_id = %s", (
                          schema_name, table_name, datetime.now(), id_record))
            banco.commit()
        return "success"
    except Exception as E:
        print(E)


def generic_insert(schema_name, table_name, record_json_path, model):
    try:
        with Database() as database:
            with open(record_json_path) as json_file:
                record: models.model = json.load(json_file)

            key_list = []
            value_list = []
            for key, value in record.items():
                key_list.append(key)
                value_list.append(value)
            
            conditions = []
            for i in range(0, len(key_list)):
                conditions.append(f"{key_list[i]} = '{value_list[i]}'")
            result = database.query(f"SELECT * FROM {schema_name}.{table_name} WHERE {' AND '.join(conditions)}")
            if not result:
                keys_string = ', '.join(key_list)
                values_string = ', '.join(f"'{value}'" for value in value_list)
                database.execute(f"INSERT INTO {schema_name}.{table_name}({keys_string}) VALUES ({values_string})")
                database.commit()
            else:
                print(f"Item já existente na tabela {table_name}.")
    except Exception as E:
        print(f"Error: {E}")


def generic_update():
    try:
        pass
    except Exception as E:
        print(E)
        
def add_states(jsonStates: Set_state):
    try:
        with Database() as banco:
            for state in jsonStates.states:
                result = banco.queryone(
                    "SELECT state_id FROM public.states WHERE state_name = %s AND state_acronym = %s", (state.state_name, state.state_acronym))
                if result:
                    pass
                else:
                    banco.execute("INSERT INTO public.states (state_name, state_acronym) VALUES(%s,%s)", (
                        state.state_name, state.state_acronym))
                    banco.commit()
        return print("Success")
    except Exception as E:
        print(E)


states = Set_state(states=[
    {"state_name": "Acre", "state_acronym": "AC"},
    {"state_name": "Alagoas", "state_acronym": "AL"},
    {"state_name": "Amapá", "state_acronym": "AP"},
    {"state_name": "Amazonas", "state_acronym": "AM"},
    {"state_name": "Bahia", "state_acronym": "BA"},
    {"state_name": "Ceará", "state_acronym": "CE"},
    {"state_name": "Distrito Federal", "state_acronym": "DF"},
    {"state_name": "Espírito Santo", "state_acronym": "ES"},
    {"state_name": "Goiás", "state_acronym": "GO"},
    {"state_name": "Maranhão", "state_acronym": "MA"},
    {"state_name": "Mato Grosso", "state_acronym": "MT"},
    {"state_name": "Mato Grosso do Sul", "state_acronym": "MS"},
    {"state_name": "Minas Gerais", "state_acronym": "MG"},
    {"state_name": "Pará", "state_acronym": "PA"},
    {"state_name": "Paraíba", "state_acronym": "PB"},
    {"state_name": "Paraná", "state_acronym": "PR"},
    {"state_name": "Pernambuco", "state_acronym": "PE"},
    {"state_name": "Piauí", "state_acronym": "PI"},
    {"state_name": "Rio de Janeiro", "state_acronym": "RJ"},
    {"state_name": "Rio Grande do Norte", "state_acronym": "RN"},
    {"state_name": "Rio Grande do Sul", "state_acronym": "RS"},
    {"state_name": "Rondônia", "state_acronym": "RO"},
    {"state_name": "Roraima", "state_acronym": "RR"},
    {"state_name": "Santa Catarina", "state_acronym": "SC"},
    {"state_name": "São Paulo", "state_acronym": "SP"},
    {"state_name": "Sergipe", "state_acronym": "SE"},
    {"state_name": "Tocantins", "state_acronym": "TO"}
])

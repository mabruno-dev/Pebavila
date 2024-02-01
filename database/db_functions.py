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

generic_insert('public', 'cities', "database/niteroi.json", "cities")

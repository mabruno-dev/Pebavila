from db_connection import Database
from datetime import datetime


def generic_delete(schema_name, table_name, id_record):
    try:
        with Database() as banco:
            banco.execute("UPDATE %s.%s SET active = 0, updated_at = %s WHERE state_id = %s", (
                          schema_name, table_name, datetime.now(), id_record))
            banco.commit()
        return "success"
    except Exception as E:
        print(E)


def generic_insert():
    try:
        with Database() as database:
            num = database.query("select * from public.states")
            print(num)
    except Exception as E:
        print(E)


def generic_update():
    try:
        pass
    except Exception as E:
        print(E)


generic_delete('public', 'states', 1)

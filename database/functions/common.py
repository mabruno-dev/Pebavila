import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))
# Resolve module imports

from utils.wrappers import announce
from utils.constants import ConsoleColors as Console
from utils.functions import print_log
from database.connection import Database

from datetime import datetime

class QueryFormatingException(Exception):
    pass

class InvalidLocationException(Exception):
    pass

def db_error(database: Database, e: Exception):
    database.connection.rollback() # Allow the connection to continue operating
    print_log(e, showDt=True, onConsole=False)
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
        db_error(database, e)

@announce
def generic_update():
    try:
        pass
    except Exception as e:
        # db_error(database, e)
        pass

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

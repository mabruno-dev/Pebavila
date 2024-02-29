import sys

import psycopg2 as postgre
from psycopg2.extras import DictCursor

class Database():

    def __init__(self, ensure_connection = False) -> None:
        try:
                self.connection = postgre.connect("""
                    dbname = 'postgres'
                    host = '25.4.215.168'
                    port = '5432'
                    user = 'postgres'
                    password = '$Pebav1la+' 
                """)
                self.cursor = self.connection.cursor(cursor_factory=DictCursor)
                print("Now connected to the database")
        except Exception as E:
            print(f'Error: {E}')
        
        if ensure_connection and not hasattr(self, "connection"):
            sys.exit()
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close(False)

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def queryone(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()
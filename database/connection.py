import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))
# Resolve module imports

from threading import Thread
from time import sleep

import psycopg2 as postgre
from psycopg2.extras import DictCursor

from utils.wrappers import timed, announce

class Database():

    def __init__(self, ensure_connection = False, persistent = False) -> None:
        
        def connect(self):
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

        def check_connection(self):
            try:
                self.cursor.execute("SELECT 1;")
                return True
            except:
                return False

        connect(self)
        
        if ensure_connection and not hasattr(self, "connection"):
            sys.exit()

        self.persistent = persistent
        if persistent:
            def reconnect(self):
                while self.persistent:
                    if not check_connection(self):
                        print("Trying to reconnect to database..")
                        connect(self)
                    else:
                        sleep(5)
            self.persistence_thread = Thread(target=reconnect, args=(self,))
            self.persistence_thread.start()
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.persistent:
            self.persistent = False
            self.persistence_thread.join()
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
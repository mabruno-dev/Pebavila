import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))
# Resolve module imports

import psycopg2 as postgre
from psycopg2.extras import DictCursor

from time import sleep
from threading import Thread, Event

from utils.constants import ConsoleColors as Console

class Database():

    def __init__(self, ensure_connection = False) -> None:
        
        stop_event = Event()
        def printer():
            aux = 0
            while not stop_event.is_set():
                if aux == 0:
                    print("", end="\r")
                    print(" "  * 50, end="\r", flush=True)
                    print("Connecting to the database", end="", flush=True)
                    aux = 3
                else:
                    print(".", end="", flush=True)
                    aux -= 1
                sleep(0.46)

        try:
            printer_thread = Thread(target=printer)
            printer_thread.start()

            self.connection = postgre.connect("""
                dbname = 'postgres'
                host = '25.11.120.164'
                port = '5432'
                user = 'postgres'
                password = '$Pebav1la+' 
            """)
            self.cursor = self.connection.cursor(cursor_factory=DictCursor)

            stop_event.set()
            printer_thread.join()
            print(Console.GREEN + "\rNow connected to the database" + Console.RESET)
        except Exception as E:
            stop_event.set()
            printer_thread.join()

            print(f'\rError: {E}')
        
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
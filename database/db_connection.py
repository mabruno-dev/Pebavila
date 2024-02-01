import psycopg2 as postgre
from psycopg2.extras import DictCursor


class Database():

    def __init__(self) -> None:
        try:
            self.connection = postgre.connect("""
                dbname=postgres
                host = '25.73.143.27'
                port = 5432
                user = 'postgres'
                password = '$Pebav1la+' 
            """)
            self.cursor = self.connection.cursor(cursor_factory=DictCursor)
        except Exception as E:
            print(f'Erro: {E}')

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

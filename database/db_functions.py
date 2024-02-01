from db_connection import Database


def states_insert():
    try:
        with Database() as database:
            num = database.query("select * from public.states")
            print(num)
    except Exception as E:
        print(E)


states_insert()
import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))
# Resolve module imports

from utils.wrappers import announce
from database.connection import Database
from database.functions.common import db_error

from datetime import datetime

@announce
def check_address_url_exists(database: Database, address_url: dict):
    try:
        return database.queryone(
            "SELECT id FROM zapimoveis.address_urls WHERE address = %s", 
            (address_url["address"],)
        )
    except Exception as e:
        db_error(database, e)
        
@announce
def insert_address_url(database: Database, address_url: dict):
    try:
        if not check_address_url_exists(database, address_url):
            database.execute(
                "INSERT INTO zapimoveis.address_urls (address, url) VALUES (%s, %s)", 
                (address_url["address"], address_url["url"])
            )
            database.commit()
            print("Record added to the database successfully")
        else:
            print("Record already exists")
    except Exception as e:
        db_error(database, e)

@announce
def update_address_url(database: Database, address_url: dict):
    try:
        if check_address_url_exists(database, address_url):
            database.execute(
                "UPDATE zapimoveis.address_urls SET url = %s, updated_at = %s WHERE address = %s",
                (address_url["url"], datetime.now(), address_url["address"])
            )
            database.commit()
            print("Record updated successfully")
    except Exception as e:
        db_error(database, e)

@announce
def get_address_urls(database: Database):
    try:
        result = database.query(
            "SELECT * FROM zapimoveis.address_urls"
        )
        address_url_list = list()
        for item in result:
            address_url = {
                "address": item[1],
                "url": item[2]
            }
            address_url_list.append(address_url)
        return address_url_list
    except Exception as e:
        db_error(database, e)

@announce
def set_address_url_scraped(database: Database, address_url: dict):
    try:
        database.execute(
            "UPDATE zapimoveis.address_urls SET scraped = 1, updated_at = %s WHERE address = %s",
            (datetime.now(), address_url["address"])
        )
        database.commit()
    except Exception as e:
        db_error(database, e)

@announce
def set_address_url_not_scraped(database: Database, address_url: dict):
    try:
        database.execute(
            "UPDATE zapimoveis.address_urls SET scraped = 0 WHERE address = %s",
            (address_url["address"],)
        )
        database.commit()
    except Exception as e:
        db_error(database, e)

@announce
def check_address_url_is_scraped(database: Database, address: str):
        try:
            result = database.queryone(
                "SELECT scraped FROM zapimoveis.address_urls WHERE address = %s",
                (address,)
            )
            return result[0]
        except Exception as e:
            db_error(database, e)


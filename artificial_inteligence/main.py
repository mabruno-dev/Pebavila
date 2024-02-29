from convert_data import convert_data_description
import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))

import numpy as np
import database
from database.db_connection import Database

data_description = convert_data_description()
database = Database()

dict = {}
i = 0
for data in data_description:

    i += 1
    dict[i] = data

all_data = database.query('SELECT * FROM realties')

for data, data_1 in zip(data_description, all_data):
    data_1 = list[data_1]
    



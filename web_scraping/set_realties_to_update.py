import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))
# Resolve module imports

from database.connection import Database
from database.functions import set_realties_not_up_to_date

database = Database()

set_realties_not_up_to_date(database)
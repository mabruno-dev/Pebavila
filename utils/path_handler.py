# PASTE THIS IN THE BEGGINING OF YOUR PYHTON SCRIPT
# TO IMPORT MODULES FROM ANOTHER FOLDER

import os
import sys

current_file = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file)
project_root = os.path.dirname(current_directory)
sys.path.append(project_root)
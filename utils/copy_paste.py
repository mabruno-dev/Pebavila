# CHANGE PYTHON PATH TO IMPORT MODULES
import os
import sys

current_file = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file)
project_root = os.path.dirname(current_directory)
sys.path.append(project_root)
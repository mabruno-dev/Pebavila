import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))
# Resolve module imports

from utils.functions import timed
from database import functions

@timed
def waste_time(n):
    result = 0
    for i in range(n):
        # Perform useless operations
        result += i ** 2  # Square of index
        result *= 2  # Double the result
        result /= 3  # Divide the result by 3
        result = result ** 0.5  # Take square root
        result -= 1  # Subtract 1
        result *= 3  # Triple the result
        result /= 2  # Divide the result by 2
        result = result ** 2  # Square the result
    return result


waste_time(767687)


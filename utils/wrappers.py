import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))
# Resolve module imports

from time import time
from io import StringIO
from functools import wraps

from utils.functions import format_time
from utils.constants import ConsoleColors as Console

def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        total_time = time() - start_time
        print(f"{func.__name__} was executed in {format_time(total_time)}")
        return result
    return wrapper

from functools import wraps
from io import StringIO
import sys

# WARNING: this breaks print statements from running threads
def announce(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        captured_output = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output

        result = func(*args, **kwargs)

        sys.stdout = old_stdout
        output = captured_output.getvalue()

        if output:
            print(Console.BLACK + f"From {func.__name__}: " + Console.RESET + output, end="", flush=True)

        return result
    return wrapper

def mute(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        captured_output = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output

        result = func(*args, **kwargs)

        sys.stdout = old_stdout

        return result
    return wrapper

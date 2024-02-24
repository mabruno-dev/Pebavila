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

# def announce(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
        
#         # Custom file-like class that writes to both stdout and a StringIO object
#         class DualOutput:
#             def __init__(self, stdout, captured):
#                 self.stdout = stdout
#                 self.captured = captured
            
#             def write(self, message):
#                 self.stdout.write(message)
#                 self.captured.write(message)
            
#             def flush(self):
#                 # This is necessary for compatibility with the file interface
#                 self.stdout.flush()
#                 self.captured.flush()

#         message = f"From {func.__name__}:"
#         print(Console.BOLD_WHITE + message + Console.RESET, end=" ")

#         captured_output = StringIO()
#         dual_output = DualOutput(sys.stdout, captured_output)
#         old_stdout = sys.stdout
#         sys.stdout = dual_output

#         result = func(*args, **kwargs)

#         sys.stdout = old_stdout

#         if not captured_output.getvalue():
#             print("\r" + " " * len(message), end="\r")

#         return result
#     return wrapper

def announce(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(Console.BLACK + f"Called {func.__name__}" + Console.RESET)
        result = func(*args, **kwargs)
        return result
    return wrapper

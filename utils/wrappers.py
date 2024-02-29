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


# Capture the original built-in print function
original_print = print

def announce(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Define a custom print function that prepends the message
        def custom_print(*pargs, **pkwargs):
            original_print(Console.BLACK + f"From {func.__name__}: " + Console.RESET, end="")
            original_print(*pargs, **pkwargs)
        
        # Check if __builtins__ is a dictionary or a module and adjust accordingly
        if isinstance(__builtins__, dict):
            # If __builtins__ is a dictionary, use dictionary methods to replace 'print'
            original_builtins_print = __builtins__['print']
            __builtins__['print'] = custom_print
        else:
            # If __builtins__ is a module, use attribute assignment
            original_builtins_print = getattr(__builtins__, 'print')
            setattr(__builtins__, 'print', custom_print)
        
        try:
            # Execute the function
            result = func(*args, **kwargs)
        finally:
            # Restore the original print function
            if isinstance(__builtins__, dict):
                __builtins__['print'] = original_builtins_print
            else:
                setattr(__builtins__, 'print', original_builtins_print)
        return result

    return wrapper

# WARNING: This will also mute running threads while the function executes
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

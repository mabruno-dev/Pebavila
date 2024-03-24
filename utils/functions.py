import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))
# Resolve module imports

import json
import inspect
from datetime import datetime

from utils.constants import ConsoleColors as Console

def format_time(seconds):
    days = seconds // (24 * 3600)
    hours = (seconds % (24 * 3600)) // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    time_str = ""
    if days:
        time_str += f"{int(days)} day{'s' if days != 1 else ''}, "
    if hours:
        time_str += f"{int(hours)} hour{'s' if hours != 1 else ''}, "
    if minutes:
        time_str += f"{int(minutes)} minute{'s' if minutes != 1 else ''}, "
    if seconds or not any((days, hours, minutes)):
        time_str += f"{seconds:.3f} second{'s' if seconds != 1 else ''}"

    return time_str

def create_dirs(file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

def get_caller_path():
    caller_frame = inspect.stack()[-1]
    calling_script_path = caller_frame.filename
    path_list = calling_script_path.split("/")
    return "/".join(path_list[(path_list.index("the-beginning") + 1):])

def print_log(text: str, showDt: bool = False, onConsole: bool = True, section: bool = False):

    caller_path = get_caller_path().replace(".py", "")

    current_date = datetime.today().strftime('%d%m%Y')
    formatted_date = datetime.today().strftime('%d/%m/%Y %H:%M:%S')

    LOG_FILE_PATH = f"logs/{caller_path}/log_{current_date}.txt"

    create_dirs(LOG_FILE_PATH)

    with open(LOG_FILE_PATH, 'a') as file:
        new_line = "\n"
        file.write(f'{text}{f"{new_line}Date: {formatted_date}" if showDt else ""}{new_line * 2}')
        if section:
            file.write("---//---\n\n")
        if onConsole:
            print(text)

def error(e):
    print(f"{Console.RED} {e}{Console.RESET}")
    print_log(e, showDt=True, onConsole=False, section=True)

print(os.path.abspath(__file__))
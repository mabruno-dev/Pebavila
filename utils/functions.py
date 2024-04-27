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

def get_caller_dir_path():
    caller_frame = inspect.stack()[-1]
    calling_script_path = caller_frame.filename.replace("\\", "/")
    path_list = calling_script_path.split("/")
    return "/".join(path_list[:-1])

def get_caller_name():
    caller_frame = inspect.stack()[-1]
    calling_script_path = caller_frame.filename.replace("\\", "/")
    path_list = calling_script_path.split("/")
    return path_list[-1]

def print_log(text: str, showDt: bool = False, onConsole: bool = True, section: bool = False):

    current_date = datetime.today().strftime('%d%m%Y')
    formatted_date = datetime.today().strftime('%d/%m/%Y %H:%M:%S')

    caller_dir_path = get_caller_dir_path().replace(".py", "").replace("/_internal", "")
    caller_name = get_caller_name().replace(".py", "")
    LOG_FILE_PATH = f"{caller_dir_path}/logs/{caller_name}/log_{current_date}.txt"

    create_dirs(LOG_FILE_PATH)

    with open(LOG_FILE_PATH, 'a') as file:
        new_line = "\n"
        file.write(f'{text}{f"{new_line * 2}Date: {formatted_date}" if showDt else ""}{new_line}')
        if section:
            file.write("\n---//---\n\n")
        if onConsole:
            print(text)

def error(e, short = False):
    error = str(e)
    if short:
        shortened_error = error.split("\n")[0]
        print(f"{Console.RED} {shortened_error}{Console.RESET}")
        print_log(shortened_error, showDt=True, onConsole=False, section=True)
    else:
        print(f"{Console.RED} {e}{Console.RESET}")
        print_log(e, showDt=True, onConsole=False, section=True)

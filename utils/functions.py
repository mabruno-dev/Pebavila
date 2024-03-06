import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))
# Resolve module imports

import json
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

def print_log(text: str, showDt: bool = False, onConsole: bool = True):

    current_date = datetime.today().strftime('%d%m%Y')
    formatted_date = datetime.today().strftime('%d/%m/%Y %H:%M:%S')

    LOG_FILE_PATH = f"log/log_{current_date}.txt"

    create_dirs(LOG_FILE_PATH)

    with open(LOG_FILE_PATH, 'a') as file:
        new_line = "\n"
        file.write(f'{text}{f"{new_line}Date: {formatted_date}" if showDt else ""}{new_line * 2}')
        if onConsole:
            print((f'{text}{f"{new_line}Date: {formatted_date}" if showDt else ""}'))

def print_error(error):
    print(Console.RED + "Error: " + Console.RESET + f"{error}")

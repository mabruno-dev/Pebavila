import os
from datetime import datetime

def format_time(seconds):
    days = seconds // (24 * 3600)
    hours = (seconds % (24 * 3600)) // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    time_str = ""
    if days:
        time_str += f"{days} day{'s' if days != 1 else ''}, "
    if hours:
        time_str += f"{hours} hour{'s' if hours != 1 else ''}, "
    if minutes:
        time_str += f"{minutes} minute{'s' if minutes != 1 else ''}, "
    if seconds or not any((days, hours, minutes)):
        time_str += f"{seconds} second{'s' if seconds != 1 else ''}"

    return time_str

def create_dirs(file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

def print_log(text: str, showDt: bool = False, showCons: bool = True):

    current_date = datetime.today().strftime('%d%m%Y')
    formatted_date = datetime.today().strftime('%d/%m/%Y %H:%M:%S')

    if not os.path.isdir('.\Log'):
        os.makedirs('.\Log')

    with open(f'.\Log\Log_{current_date}.txt', 'a') as file:
        file.write(f'{text}{f" | {formatted_date}" if showDt else ""}\n')
        if showCons:
            print((f'{text}{f" | {formatted_date}" if showDt else ""}'))
        file.close()
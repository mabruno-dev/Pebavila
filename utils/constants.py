from random import choice

class RealtyConstants:
    DONE = 2
    FLOOR_PLAN = 0
    UNDER_CONSTRUCTION = 1
    FURNISHED = True
    NOT_FURNISHED = False

class ConsoleColors:
    RESET = "\033[0m"

    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    WHITE = "\033[0;37m"

    BOLD_BLACK = "\033[1;30m"
    BOLD_RED = "\033[1;31m"
    BOLD_GREEN = "\033[1;32m"
    BOLD_YELLOW = "\033[1;33m"
    BOLD_BLUE = "\033[1;34m"
    BOLD_PURPLE = "\033[1;35m"
    BOLD_CYAN = "\033[1;36m"
    BOLD_WHITE = "\033[1;37m"

    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_PURPLE = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

    @staticmethod
    def random_color():
        # Get all color attributes from the class
        colors = [attr for attr in dir(ConsoleColors) if not callable(getattr(ConsoleColors, attr)) and not attr.startswith("__")]
        # Remove RESET attribute
        colors.remove("RESET")
        # Choose a random color from the list
        random_color = getattr(ConsoleColors, choice(colors))
        return random_color


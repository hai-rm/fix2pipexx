class colors:
    RED = '\033[31m'
    RED_BACK = '\033[101m'
    GREEN = '\033[32m'
    ORANGE = '\033[33m'
    ORANGE_BACK = '\033[30;43m'
    BLUE = '\033[34m'
    BLUE_BACK = '\033[44m'
    MAGENTA = '\033[35m'
    MAGENTA_BACK = '\033[45m'
    CYAN = '\033[36m'
    CYAN_BACK = '\033[106m'
    GRAY = '\033[37m'
    GRAY_BACK = '\033[100m'
    GREEN_BACK = '\033[30;42m'
    DARK_GRAY = '\033[90m'
    DARK_GRAY_BACK = '\033[100m'
    PINK = '\033[38;5;199m'
    PINK_BACK = '\033[48;5;199m'
    YELLOW = '\033[93m'
    YELLOW_BACK = '\033[30;103m'
    WHITE = '\033[97m'
    ENDCOLOR = '\033[0m'


def print_color(color, txt):
    print(color + txt + colors.ENDCOLOR)


def print_error(txt):
    print_color(colors.RED, "ERROR: " + txt)


def print_warning(txt):
    print_color(colors.ORANGE, "WARNING: " + txt)


def print_info(txt):
    print_color(colors.GRAY, "INFO: " + txt)

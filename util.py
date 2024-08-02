class colors:
    RED = '\033[31m'
    GREEN = '\033[32m'
    ORANGE = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    GRAY = '\033[37m'
    GRAY_BACK = '\033[100m'
    TEAL_BACK = '\033[106m'
    ENDCOLOR = '\033[0m'


def print_color(color, txt):
    print(color + txt + colors.ENDCOLOR)


def print_error(txt):
    print_color(colors.RED, "ERROR: " + txt)


def print_warning(txt):
    print_color(colors.ORANGE, "WARNING: " + txt)


def print_info(txt):
    print_color(colors.GRAY, "INFO: " + txt)

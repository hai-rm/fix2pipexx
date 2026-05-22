class colors:
    RED = "\033[31m"
    RED_BACK = "\033[101m"
    GREEN = "\033[32m"
    ORANGE = "\033[33m"
    ORANGE_BACK = "\033[30;43m"
    BLUE = "\033[34m"
    BLUE_BACK = "\033[44m"
    MAGENTA = "\033[35m"
    MAGENTA_BACK = "\033[45m"
    CYAN = "\033[36m"
    CYAN_BACK = "\033[106m"
    GRAY = "\033[37m"
    GRAY_BACK = "\033[100m"
    GREEN_BACK = "\033[30;42m"
    DARK_GRAY = "\033[90m"
    DARK_GRAY_BACK = "\033[100m"
    PINK = "\033[38;5;199m"
    PINK_BACK = "\033[48;5;199m"
    YELLOW = "\033[93m"
    YELLOW_BACK = "\033[30;103m"
    WHITE = "\033[97m"
    ENDCOLOR = "\033[0m"


def print_color(color, txt):
    print(color + txt + colors.ENDCOLOR)


def print_error(txt):
    print_color(colors.RED, "ERROR: " + txt)


def print_warning(txt):
    print_color(colors.ORANGE, "WARNING: " + txt)


def print_info(txt):
    print_color(colors.GRAY, "INFO: " + txt)


tag_value_descriptions = {
    # MsgType
    35: {
        "0": "Heartbeat",
        "1": "Test Request",
        "3": "Reject",
        "4": "Sequence Reset",
        "5": "Logout",
        "8": "Execution Report",
        "9": "Order Cancel Reject",
        "A": "Logon",
        "AB": "New Order Multileg",
        "AD": "Trade Capture Report Request",
        "AE": "Trade Capture Report",
        "AI": "Quote Status Report",
        "AQ": "Trade Capture Report Request Ack",
        "AR": "Trade Capture Report Ack",
        "D": "New Order Single",
        "F": "Order Cancel Request",
        "G": "Order Cancel/Replace Request",
        "Q": "Dont Know Trade",
        "R": "Quote Request",
        "S": "Quote",
        "V": "Market Data Request",
        "W": "Market Data Snapshot",
        "X": "Market Data Incremental",
        "Y": "Market Data Request Reject",
        "Z": "Quote Cancel",
        "a": "Quote Status Request",
        "b": "Quote Ack",
        "d": "Security Definition",
        "g": "Trading Session Status Request",
        "h": "Trading Session Status",
        "i": "Mass Quote",
        "j": "Business Message Reject",
    },
    # OrdStatus
    39: {
        "0": "New",
        "1": "Partially filled",
        "2": "Filled",
        "3": "Done for day",
        "4": "Canceled",
        "5": "Replaced",
        "6": "Pending Cancel",
        "7": "Stopped",
        "8": "Rejected",
        "9": "Suspended",
        "A": "Pending New",
        "B": "Calculated",
        "C": "Expired",
        "D": "Accepted for bidding",
        "E": "Pending Replace",
    },
    # OrdType
    40: {
        "1": "Market",
        "2": "Limit",
        "3": "Stop",
        "4": "Stop limit",
        "D": "Previously quoted",
        "E": "Previously indicated",
        "F": "Forex limit - deprecated",
        "H": "Forex quoted - deprecated",
    },
    # Side
    54: {
        "0": "None",
        "1": "Buy",
        "2": "Sell",
    },
    # TimeInForce
    59: {
        "0": "Day",
        "1": "GTC - Good Till Cancel",
        "3": "IOC - Immediate Or Cancel",
        "4": "FOK - Fill Or Kill",
        "6": "Good Till Date",
        "7": "Week",
    },
    # ExecType
    150: {
        "0": "New",
        "1": "Partial Fill - deprecated",
        "2": "Fill - deprecated",
        "3": "Done For Day",
        "4": "Canceled",
        "5": "Replaced",
        "6": "Pending Cancel",
        "7": "Stopped",
        "8": "Rejected",
        "A": "Pending New",
        "B": "Calculated",
        "C": "Expired",
        "D": "Restated",
        "E": "Pending Replace",
        "F": "Trade - Fill or Partial Fill",
    },
    # QuoteStatus
    297: {
        "0": "Accepted",
        "1": "Canceled for Symbol",
        "4": "Canceled All",
        "5": "Rejected",
        "7": "Expired",
    },
    # QuoteCancelType
    298: {
        "1": "Cancel for Symbol",
        "4": "Cancel All Quotes",
    },
    # TradSesStatus
    340: {
        "1": "Halted",
        "2": "Open",
        "3": "Closed",
        "4": "Pre-Open",
        "5": "Pre-Close",
    },
}


def describe_field(key, val):
    if key in tag_value_descriptions:
        key_desc = tag_value_descriptions[key]
        if val in key_desc:
            return "(" + key_desc[val] + ")"
    return ""

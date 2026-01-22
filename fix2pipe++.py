#!/usr/bin/env python

import re, sys, argparse
from validate_rfq import *


def parse_tags_file(tags_filename):
    tags_map = {}
    tags_file = open(tags_filename, "r")
    tags_file_content = tags_file.read()
    result = re.search(r"enum class Tag : int \{([\s\S]*?)\};",
                       tags_file_content)
    if result:
        for line in result.groups()[0].splitlines():
            line = line.strip()
            if line[:2] == "//":
                continue
            tag_name_and_value = line.split("=")
            if len(tag_name_and_value) == 2:
                tag_name = tag_name_and_value[0]
                value = tag_name_and_value[1]
                tags_map[int(value.strip(" ,"))] = tag_name.strip()
    else:
        print("Error parsing tags file " + tags_filename)

    return tags_map


def tag_key(t):
    return t[0]


def name_key(t):
    return t[1]


tag_value_descriptions = {
    # Side
    54: {
        "0": "None",
        "1": "Buy",
        "2": "Sell",
    },
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
        "F": "Forex Limit - deprecated"
    },
    # TimeInForce
    59: {
        "0": "Day",
        "1": "GTC - Good Till Cancel",
        "3": "IOC - Immediate Or Cancel",
        "6": "Good Till Date",
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
        "F": "Trade - Fill or Partial Fill"
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


def print_fix_msg(msg_map, tags_map, direction, sort_by):
    msg_fields = []
    for key, value in msg_map.items():
        name = ""
        if not tags_map is None and key in tags_map.keys():
            name = tags_map[key]
        msg_fields.append((key, name, value))

    if sort_by == "name" and not tags_map is None:
        msg_fields.sort(key=name_key)
    else:
        msg_fields.sort(key=tag_key)

    outgoing = False
    if direction == "incoming":
        print(colors.PINK +
              f"INCOMING             []  <------------ {msg_map.get(35)}" +
              colors.ENDCOLOR)
        color_str = colors.WHITE
    elif direction == "outgoing":
        outgoing = True
        print(colors.PINK_BACK +
              f"OUTGOING             []  {msg_map.get(35)} ------------>" +
              colors.ENDCOLOR)
        color_str = colors.GRAY_BACK
    else:
        color_str = colors.GRAY

    if "8" in msg_map.get(35) and ("F" in msg_map.get(150)
                                   or "1" in msg_map.get(150)
                                   or "2" in msg_map.get(150)):
        color_str = colors.GREEN_BACK if outgoing else colors.GREEN

    if "8" in msg_map.get(35) and ("3" in msg_map.get(150)
                                   or "B" in msg_map.get(150)):
        color_str = colors.YELLOW_BACK if outgoing else colors.YELLOW

    if "8" in msg_map.get(35) and "8" in msg_map.get(150):
        color_str = colors.RED_BACK if outgoing else colors.RED

    if "8" in msg_map.get(35) and ("4" in msg_map.get(150)
                                   or "C" in msg_map.get(150)):
        color_str = colors.ORANGE_BACK if outgoing else colors.ORANGE

    if "8" in msg_map.get(35) and "5" in msg_map.get(150):
        color_str = colors.CYAN_BACK if outgoing else colors.CYAN

    if "D" in msg_map.get(35) or "AB" in msg_map.get(35):
        color_str = colors.BLUE_BACK if outgoing else colors.BLUE

    if "G" in msg_map.get(35):
        color_str = colors.CYAN_BACK if outgoing else colors.CYAN

    if "R" in msg_map.get(35):
        color_str = colors.YELLOW_BACK if outgoing else colors.YELLOW

    if "S" in msg_map.get(35):
        color_str = colors.MAGENTA_BACK if outgoing else colors.MAGENTA

    if "Z" in msg_map.get(35) or "F" in msg_map.get(35):
        color_str = colors.ORANGE_BACK if outgoing else colors.ORANGE

    if ("3" in msg_map.get(35) or "AG" in msg_map.get(35)
        or "Y" in msg_map.get(35) or "9" in msg_map.get(35)):
        color_str = colors.RED_BACK if outgoing else colors.RED

    for key, name, value in msg_fields:
        description = ""
        if len(value) == 1:
            value_str = str(value[0])
            description = describe_field(key, value_str)
        else:
            value_str = '[' + ', '.join(value) + ']'

        output = "{0:6} {1:28} {2} {3}".format(key, name, value_str,
                                               description)
        print_color(color_str, output)


def parse_fix_msg(msg, tags_map, direction, sort_by):
    msg_map = {}
    fields = msg.split("|")
    for field in fields:
        if len(field) > 0:
            tag_value = field.split("=", 1)
            if len(tag_value) != 2 or not tag_value[0].isdigit():
                continue

            tag = int(tag_value[0])
            value = tag_value[1].strip(" ,\x01")
            if not tag in msg_map:
                msg_map[tag] = []
            msg_map[tag].append(value)

    print_fix_msg(msg_map, tags_map, direction, sort_by)

def highlight_patterns(line):
    line = re.sub(r"(,Accnt[^,]*)", f"{colors.RED}\\1{colors.ENDCOLOR}", line)
    line = re.sub(r"(,OrderID[^,]*)", f"{colors.RED}\\1{colors.ENDCOLOR}", line)
    line = re.sub(r"(,OrderStatus[^,]*)", f"{colors.CYAN}\\1{colors.ENDCOLOR}", line)
    line = re.sub(r"(,Tenor[^,]*)", f"{colors.ORANGE}\\1{colors.ENDCOLOR}", line)
    line = re.sub(r"(,FixingDate[^,]*)", f"{colors.ORANGE}\\1{colors.ENDCOLOR}", line)
    line = re.sub(r"(,SettlDate[^,]*)", f"{colors.ORANGE}\\1{colors.ENDCOLOR}", line)
    line = re.sub(r"(,LastFwdPoints[^,]*)", f"{colors.ORANGE}\\1{colors.ENDCOLOR}", line)
    line = re.sub(r"(,ExecType[^,]*)", f"{colors.GREEN}\\1{colors.ENDCOLOR}", line)
    line = re.sub(r"(,QtyType[^,]*)", f"{colors.MAGENTA}\\1{colors.ENDCOLOR}", line)
    line = re.sub(r"(,Side[^,]*)", f"{colors.MAGENTA}\\1{colors.ENDCOLOR}", line)
    line = re.sub(r"(,ResdQty[^,]*)", f"{colors.BLUE}\\1{colors.ENDCOLOR}", line)
    line = re.sub(r"(,CumQty[^,]*)", f"{colors.BLUE}\\1{colors.ENDCOLOR}", line)
    line = re.sub(r"(,CumCost[^,]*)", f"{colors.BLUE}\\1{colors.ENDCOLOR}", line)
    line = re.sub(r"(,LastPrice[^,]*)", f"{colors.BLUE}\\1{colors.ENDCOLOR}", line)

    line = re.sub(r"(ERROR)", f"{colors.RED_BACK}\\1{colors.ENDCOLOR}", line)
    line = re.sub(r"(WARN)", f"{colors.ORANGE_BACK}\\1{colors.ENDCOLOR}", line)
    line = re.sub(r"(INFO)", f"{colors.GREEN_BACK}\\1{colors.ENDCOLOR}", line)

    return line


def parse_line(line, tags_map, only_fix, sort_by):
    line = line.replace("\x01", "|")
    direction_regex = re.search("(incoming|outgoing)", line)
    direction = direction_regex.groups()[0] if direction_regex is not None else "unknown"

    result = re.search("(35=.*10=.*)", line)

    if not only_fix:
        print(highlight_patterns(line), end="")

    if result:
        msg = result.groups()[0]
        parse_fix_msg(msg, tags_map, direction, sort_by)
        if only_fix:
            print("------------------------------------------------------")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="fix2pipe++ fix parser",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-t", "--tags", help="path to Tag.hpp")
    parser.add_argument("-o",
                        "--only-fix",
                        action="store_true",
                        help="only outputs formatted fix")
    parser.add_argument(
        "-s",
        "--sort-by",
        choices=["tag", "name"],
        default="tag",
        help="sorts fields by tag number or name",
    )

    args = parser.parse_args()
    config = vars(args)

    tags_map = None
    if config["tags"]:
        tags_map = parse_tags_file(config["tags"])

    only_fix = config["only_fix"]
    sort_by = config["sort_by"]

    for line in sys.stdin:
        parse_line(line, tags_map, only_fix, sort_by)

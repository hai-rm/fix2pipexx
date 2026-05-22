#!/usr/bin/env python

import re, sys, argparse
from validate_rfq import *
from util import describe_field


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

    if direction == "incoming":
        print(f"INCOMING             []  <------------ {msg_map.get(35)}")
    else:
        print(f"OUTGOING             []  {msg_map.get(35)} ------------>")

    for key, name, value in msg_fields:
        description = ""
        if len(value) == 1:
            value_str = str(value[0])
            description = describe_field(key, value_str)
        else:
            value_str = '[' + ', '.join(value) + ']'

        output = "{0:6} {1:28} {2} {3}".format(key, name, value_str,
                                               description)
        print(output)


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


def parse_line(line, tags_map, only_fix, sort_by):
    line = line.replace("\x01", "|")
    direction_regex = re.search("(incoming|outgoing)", line)
    direction = direction_regex.groups()[0] if direction_regex is not None else "unknown"

    result = re.search("(35=.*10=.*)", line)

    if not only_fix:
        print(line, end="")

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

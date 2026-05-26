#!/usr/bin/env python3

from get_config import get_config


def main() -> None:
    logo = {"1000111",
            "1000001",
            "1110111",
            "0010100",
            "0010111"}
    logo = logo
    a = get_config("config.txt")
    print(a)
    width = a["WIDTH"]
    height = a["HEIGHT"]
    b = ["oooo", "0   ", "1111"]

    # test printing a map
    for x in range(height):
        for y in range(width):
            if y == 1 and x == 1:
                print(b[2], end="")
            else:
                print(b[0], end="")
        print("o")
        for y in range(width):
            print(b[1], end="")
        print("0")
    for y in range(width):
        print(b[0], end="")
    print("o")


if __name__ == "__main__":
    main()


"""
def parse_value(key, value):
    value = value.strip()

    # tuple values like ENTRY=0,0
    if key in {"ENTRY", "EXIT()"}:
        return tuple(map(int, value.split(",")))

    # booleans
    if value.lower() == "true":
        return True

    if value.lower() == "false":
        return False

    # integers
    if value.isdigit():
        return int(value)

    # strings
    return value


def load_config(filename):
    config = {}

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()

            # skip empty lines
            if not line:
                continue

            key, value = line.split("=", 1)
            config[key] = parse_value(key, value)

    return config


config = load_config("data.txt")

print(config)

# usage examples
width = config["WIDTH"]
height = config["HEIGHT"]
entry = config["ENTRY"]
exit()_pos = config["EXIT()"]
output_file = config["OUTPUT_FILE"]
perfect = config["PERFECT"]
seed = config["SEED"]

print(width)
print(entry)
print(perfect)
"""

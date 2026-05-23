#!/usr/bin/env python3

from maze_map import map_creator, Cell
import sys


def atributor_start(map: list[list[Cell]], xy: list[int]) -> list[list[Cell]]:
    """Create the entry"""
    map[xy[0]][xy[1]].is_start = True


def atributor_exit(map: list[list[Cell]], xy: list[int]) -> list[list[Cell]]:
    """Create the exit and check overlapping with the entry"""
    try:
        map[xy[0]][xy[1]].is_exit = True
        if map[xy[0]][xy[1]].is_start:
            raise ValueError("Overlaping roles: Entry and Exit")
    except ValueError as err:
        print(err)
        sys.exit()


# define as 42 cell
# reusable for other general modifications and detections like the bonus
# Last initialisator to pass, to avoid overlaping ****
def fourtier(map: list[list[Cell]], height: int, width: int) -> list[list[Cell]]:
    """create the 42 logo and check overlaping with entry and exit"""
    logo = ["1000111",
            "1000001",
            "1110111",
            "0010100",
            "0010111"]
    start_o = int((width - 7) / 2)
    start_v = int((height - 5) / 2)
    try:
        for x in range(5):
            for y in range(7):
                if map[start_v + x][start_o + y].is_start:
                    raise ValueError("Overlaping roles: Entry and 42")
                if map[start_v + x][start_o + y].is_exit:
                    raise ValueError("Overlaping roles: Exit and 42")
                map[start_v + x][start_o + y].is_ft = int(logo[x][y])  # **** may cause a mypy error later
                map[start_v + x][start_o + y].visited = int(logo[x][y])
    except ValueError as err:
        print(err)
        sys.exit()


def ariane_string(map: list[list[Cell]], the_way: list[list[int]]):
    """Create the exit way"""
    for x, y in the_way:
        map[y][x].is_way_out = 1


def main() -> None:
    from get_config import get_config
    a = get_config("config.txt")
    a = a
    width = 12
    height = 12
    start = [1, 2]
    exit = [9, 10]

    map = map_creator(height, width)
    fourtier(map, height, width)
    atributor_start(map, start)
    atributor_exit(map, exit)

    for x in range(height):
        for y in range(width):
            if map[x][y].is_ft == 1:
                print("XXXX", sep="", end="")
            else:
                print(map[x][y].upper_closed, sep="", end="")
        print("o\n", end="")

        for y in range(width):
            if map[x][y].is_ft == 1:
                print("0000", sep="", end="")
            elif map[x][y].is_start == 1:
                print("0SSS", sep="", end="")
            elif map[x][y].is_exit == 1:
                print("0EEE", sep="", end="")
            else:
                print(map[x][y].middle_closed, sep="", end="")
        print("0\n", end="")

    print("oooo" * width, "o\n", sep="", end="")

    print("Hexa =", map[0][0].hexa)
    print("Total wall =", map[0][0].total_wall)


if __name__ == "__main__":
    main()

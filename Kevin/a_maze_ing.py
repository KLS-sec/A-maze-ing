#!/usr/bin/env python3

from get_config import get_config
from maze_map import maze_creator
import role_atribution
import way_maker
import imperfect_maze


def main() -> None:
    config = get_config("config.txt")
    print(config, "\n")

    maze = maze_creator(config["HEIGHT"], config["WIDTH"])
    print("Maze size:", len(maze), "time", len(maze[0]), "\n")

    role_atribution.atributor_start(maze, config["ENTRY"])
    role_atribution.atributor_exit(maze, config["EXIT"])
    role_atribution.fourtier(maze, config["HEIGHT"], config["WIDTH"])
    print("Atribution done\n")
    # width = config["WIDTH"]
    # height = config["HEIGHT"]

    way_maker.wanderer(maze, config["ENTRY"], config)
    # for y in range(config["HEIGHT"]):
    #    for x in range(config["WIDTH"]):
    #        print(maze[y][x].get_hexa(), sep="", end=" ")
    #    print("")

    if not config["PERFECT"]:
        imperfect_maze.imperfect_maker(maze, config)
        imperfect_maze.imperfect_solver(maze, config)

    for y in range(config["HEIGHT"]):
        for x in range(config["WIDTH"]):
            """if maze[y][x].is_way_out and not maze[y][x].is_start and not maze[y][x].is_exit:
                print("oooo", sep="", end="")
            else:"""
            print(maze[y][x].get_upper_wall(maze, x, y)[0], maze[y][x].get_upper_wall(maze, x, y)[1], sep="", end="")
        print(maze[y][x].left_closed, "\n", end="")
        for x in range(config["WIDTH"]):
            """if maze[y][x].is_way_out and not maze[y][x].is_start and not maze[y][x].is_exit:
                print("0...", sep="", end="")
            else:"""
            print(maze[y][x].get_left_wall(maze, x, y)[0], maze[y][x].get_left_wall(maze, x, y)[1], sep="", end="")
        print("0\n", end="")

    print(maze[y][x].left_closed * 4 * config["WIDTH"], maze[y][x].left_closed, "\n", sep="", end="")

    # hexadecimal
    print("Hexa =", hex(maze[0][0].get_hexa())[2:])
    print("Bin =", bin(maze[0][0].get_hexa())[2:])
    print("Total wall =", maze[0][0].get_wallnumber())


"""
def main() -> None:

    for x in range(height):
        for y in range(width):
            if maze[x][y].is_ft == 1:
                print("XXXX", sep="", end="")
            else:
                print(maze[x][y].upper_closed, sep="", end="")
        print("o\n", end="")

        for y in range(width):
            if maze[x][y].is_ft == 1:
                print("0000", sep="", end="")
            elif maze[x][y].is_start == 1:
                print("0SSS", sep="", end="")
            elif maze[x][y].is_exit == 1:
                print("0EEE", sep="", end="")
            else:
                print(maze[x][y].left_closed, sep="", end="")
        print("0\n", end="")

    print("oooo" * width, "o\n", sep="", end="")

    print("Hexa =", maze[0][0].get_hexa())
    print("Total wall =", maze[0][0].get_wallnumber())
"""

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

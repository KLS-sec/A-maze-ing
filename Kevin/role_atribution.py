#!/usr/bin/env python3

from maze_map import maze_creator, Cell
import sys

# checked, should be complete


def atributor_start(maze: list[list[Cell]], start: list[int]) -> None:
    """Create the entry"""
    maze[(start[0])][(start[1])].is_start = True


def atributor_exit(maze: list[list[Cell]], exit: list[int]) -> None:
    """Create the exit and check overlapping with the entry"""
    try:
        maze[exit[0]][exit[1]].is_exit = True
        if maze[exit[0]][exit[1]].is_start:
            raise ValueError("Overlaping roles: Entry and Exit")
    except ValueError as err:
        print(err)
        sys.exit()


def fourtier(maze: list[list[Cell]], height: int, width: int) -> None:
    """Create the 42 logo and check overlaping with entry and exit.

    Use a list of str to atribute the if_ft status and draw the 42 logo in the
    middle of the maze.
    Check for overlapping with start and exit.
    Systeme adaptable for other kinds of Cell mapping.
    Also give the "visited" atribute to stop the cells from opening.
    """
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
                if maze[start_v + x][start_o + y].is_start:
                    raise ValueError("Overlaping roles: Entry and 42")
                if maze[start_v + x][start_o + y].is_exit:
                    raise ValueError("Overlaping roles: Exit and 42")
                maze[start_v + x][start_o + y].is_ft = int(logo[x][y])  # **** may cause a mypy error later
                maze[start_v + x][start_o + y].is_visited = int(logo[x][y])
    except ValueError as err:
        print(err)
        sys.exit()


def ariane_string(maze: list[list[Cell]], the_way: list[list[int]]):
    """Create the exit way

    Take the list of coordinates leading to the exit and change the atribute
    is_way_out"""
    for x, y in the_way:
        maze[y][x].is_way_out = 1


def main() -> None:
    from get_config import get_config
    a = get_config("config.txt")
    a = a
    width = 12
    height = 12
    start = [1, 2]
    exit = [9, 10]

    maze = maze_creator(height, width)
    fourtier(maze, height, width)
    atributor_start(maze, start)
    atributor_exit(maze, exit)

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


if __name__ == "__main__":
    main()

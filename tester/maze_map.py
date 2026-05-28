#!/usr/bin/env python3

from dataclasses import dataclass


# Mostly done, rest the last 2 bonuses
# **** add the filled and the empty propriety
@dataclass
class Cell:
    """Create a Cell of the maze, pilot the other functions.

    Store the differents states of the cells, return the hexadecimal, memorise
    which wall are open or closed, return the needed prints.

    Potential amelioration:
        Can be enhenced by automatising the implementation of new properties.
    """
    # The different appearences for the walls depending on the cell state.
    # Normal
    upper_left: str = "█"
    upper_closed: str = "■■■"
    upper_open: str = "   "
    left_closed: str = "█"
    left_open: str = " "
    center: str = "   "

    # Forty-two
    upper_is_ft: str = "███"
    upper_left_is_ft: str = "█"
    left_is_ft: str = "█"
    center_is_ft: str = "███"

    # Start
    center_is_start: str = "███"

    # Exit
    center_is_exit: str = "███"

    # Way out
    upper_is_way_out: str = " ■ "
    left_is_way_out: str = "■"
    center_is_way_out: str = " ■ "

    is_ft: bool = 0
    is_start: bool = 0
    is_exit: bool = 0
    is_way_out: bool = 0
    is_visited: bool = 0

    north: bool = 1
    east: bool = 1
    south: bool = 1
    west: bool = 1

    def get_hexa(self) -> int:
        # Return the hexadecimal value.
        return (self.north * 1 + self.east * 2 + self.south * 4 +
                self.west * 8)

    def get_wallnumber(self) -> int:
        # Return the number of closed wall for the imperfect maze.
        return (self.north + self.east + self.south + self.west)

    def get_upper_wall(self, maze: list[list["Cell"]], x: int, y: int, show_path: bool) -> dict[str, str]:
        # Return the upper wall to print depending on the cell location.
        upper_wall = {}
        # upper-left
        # ft
        if (self.is_ft or ((maze[y - 1][x].is_ft or maze[y - 1][x - 1].is_ft)
                           and y != 0) or (maze[y][x - 1].is_ft and x != 0)):
            upper_wall["upper_left_is_ft"] = self.upper_left_is_ft
        # normal
        else:
            upper_wall["upper_left"] = self.upper_left

        # upper middle
        # ft
        if (self.is_ft or (maze[y - 1][x].is_ft and y != 0)):
            upper_wall["upper_is_ft"] = self.upper_is_ft
        # closed
        elif self.north == 1:
            upper_wall["upper_closed"] = self.upper_closed
        elif self.is_way_out == 1 and maze[y - 1][x].is_way_out == 1:  # **** add the conditionnal to trigger the coloration
            if show_path:
                upper_wall["upper_is_way_out"] = self.upper_is_way_out
            else:
                upper_wall["upper_is_way_out"] = "   "
        # normal
        else:
            upper_wall["upper_open"] = self.upper_open

        return upper_wall

        """
        if self.is_ft or (maze[y - 1][x].is_ft and y != 0):
            return self.upper_ft
        elif maze[y - 1][x - 1].is_ft or maze[y][x - 1].is_ft:
            return self.upper_left_is_ft

        if self.is_start or (maze[y - 1][x].is_start and y != 0):
            return self.upper_start
        elif (maze[y - 1][x - 1].is_start and x != 0 and
              y != 0) or (maze[y][x - 1].is_start and x != 0):
            return self.upper_left_is_start

        if self.is_exit or (maze[y - 1][x].is_exit and y != 0):
            return self.upper_exit
        elif (maze[y - 1][x - 1].is_exit and x != 0 and
              y != 0) or (maze[y][x - 1].is_exit and x != 0):
            return self.upper_left_is_exit

        elif self.north:
            return self.upper_closed
        else:
            return self.upper_open"""

    def get_left_wall(self, maze: list[list["Cell"]], x: int, y: int, show_path: bool) -> dict[str, str]:
        # Return the left wall to print depending on the cell location.
        left_center = {}
        # left
        if self.is_ft or maze[y][x - 1].is_ft:
            left_center["left_is_ft"] = self.left_is_ft
        elif self.west == 1:
            left_center["left_closed"] = self.left_closed
        elif self.is_way_out == 1 and (maze[y][x - 1].is_way_out == 1 or maze[y][x - 1].is_exit == 1 or maze[y][x - 1].is_start == 1):
            if show_path:
                left_center["left_is_way_out"] = self.left_is_way_out
            else:
                left_center["left_is_way_out"] = " "
        else:
            left_center["left_open"] = self.left_open

        # center
        if self.is_ft:
            left_center["center_is_ft"] = self.center_is_ft
        elif self.is_start:
            left_center["center_is_start"] = self.center_is_start
        elif self.is_exit:
            left_center["center_is_exit"] = self.center_is_exit
        elif self.is_way_out:
            if show_path:
                left_center["center_is_way_out"] = self.center_is_way_out
            else:
                left_center["center_is_way_out"] = "   "
        # elif self.is_way_out:  # **** can be conditionned
        else:
            left_center["center"] = self.center

        return left_center


def maze_creator(height: int, width: int) -> list[list[Cell]]:
    """Create all the Cell and return them in a list of list."""
    maze = []
    for _ in range(height):
        row = []
        for _ in range(width):
            row.append(Cell())
        maze.append(row)
    return maze


def main() -> None:
    from get_config import get_config
    from role_atribution import fourtier
    a = get_config("config.txt")
    width = a["WIDTH"]
    height = a["HEIGHT"]

    maze = maze_creator(height, width)
    maze[9][12].is_start = True
    maze[1][3].is_exit = True
    fourtier(maze, height, width)

    for y in range(height):
        for x in range(width):
            print(maze[y][x].get_upper_wall(maze, x, y), sep="", end="")
        print("o\n", end="")
        for x in range(width):
            print(maze[y][x].get_left_wall(maze, x, y), sep="", end="")
        print("0\n", end="")

    print("oooo" * width, "o\n", sep="", end="")
    print("Hexa =", maze[0][0].get_hexa())
    print("Total wall =", maze[0][0].get_wallnumber())


if __name__ == "__main__":
    main()

"""
from abc import ABC, abstractmethod

class Creature(ABC):
    def __init__(self, name: str, type: str) -> None:
        self._name: str = name
        self._type: str = type

    @abstractmethod
    def attack(self) -> str:
        pass

    def describe(self) -> str:
        return (f"{self._name} is a {self._type} type creature")


class Flameling(Creature):
    def __init__(self) -> None:
        super().__init__("Flameling", "Fire")

    def attack(self) -> str:
        return ("Flameling uses Ember!")
"""

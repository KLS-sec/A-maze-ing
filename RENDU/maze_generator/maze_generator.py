import random
import sys
from pydantic import BaseModel, Field, model_validator, ValidationError
import re
from typing import List
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
    upper_left: str = "o"
    upper_closed: str = "ooo"
    upper_open: str = "   "
    left_closed: str = "o"
    left_open: str = " "
    center: str = "   "

    # Forty-two
    upper_is_ft: str = "444"
    upper_left_is_ft: str = "4"
    left_is_ft: str = "4"
    center_is_ft: str = "444"

    # Start
    center_is_start: str = "sss"

    # Exit
    center_is_exit: str = "eee"

    # Way out
    upper_is_way_out: str = " w "
    left_is_way_out:  str = "w"
    center_is_way_out: str = " w "

    is_ft: bool = False
    is_start: bool = False
    is_exit: bool = False
    is_way_out: bool = False
    is_visited: bool = False

    north: bool = True
    east: bool = True
    south: bool = True
    west: bool = True

    def get_hexa(self) -> str:
        # Return the hexadecimal value.
        return format(
            self.north * 1 + self.east * 2 + self.south * 4 + self.west * 8,
            "X"
        )

    def get_wallnumber(self) -> int:
        # Return the number of closed wall for the imperfect maze.
        return (self.north + self.east + self.south + self.west)

    def get_upper_wall(self, maze: list[list["Cell"]], x: int, y: int,
                       show_path: bool) -> dict[str, str]:
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
        elif self.is_way_out == 1 and maze[y - 1][x].is_way_out == 1:  # ****
            # add the conditionnal to trigger the coloration
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

    def get_left_wall(self, maze: list[list["Cell"]], x: int, y: int,
                      show_path: bool) -> dict[str, str]:
        # Return the left wall to print depending on the cell location.
        left_center = {}
        # left
        if self.is_ft or maze[y][x - 1].is_ft:
            left_center["left_is_ft"] = self.left_is_ft
        elif self.west == 1:
            left_center["left_closed"] = self.left_closed
        elif self.is_way_out == 1 and (maze[y][x - 1].is_way_out == 1 or
                                       maze[y][x - 1].is_exit == 1 or
                                       maze[y][x - 1].is_start == 1):
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


# def main() -> None:
#     from get_config import get_config
#     from role_atribution import fourtier
#     a = get_config("config.txt")
#     width = a.width
#     height = a.height

#     maze = maze_creator(height, width)
#     maze[9][12].is_start = True
#     maze[1][3].is_exit = True
#     fourtier(maze, height, width)

#     for y in range(height):
#         for x in range(width):
#             print(maze[y][x].get_upper_wall(maze, x, y), sep="", end="")
#         print("o\n", end="")
#         for x in range(width):
#             print(maze[y][x].get_left_wall(maze, x, y), sep="", end="")
#         print("0\n", end="")

#     print("oooo" * width, "o\n", sep="", end="")
#     print("Hexa =", maze[0][0].get_hexa())
#     print("Total wall =", maze[0][0].get_wallnumber())


# if __name__ == "__main__":
#     main()

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

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


class Config():
    width: int = 0
    height: int = 0
    entry: list[int]
    exit: list[int]
    output_file: str = "output_maze.txt"
    perfect: bool = True
    seed: bool = False
    path: list[list[int]]  # ****


class config_storage(BaseModel):
    """Multiple check for the config file input."""
    width: int = Field(ge=2, le=50)
    height: int = Field(ge=2, le=20)
    entry: list[int]
    exit: list[int]
    output_file: str
    perfect: bool

    @model_validator(mode='after')
    def checker(self) -> "config_storage":
        if len(self.entry) != 2:
            raise ValueError("Entry error, invalid coordinates")
        if len(self.exit) != 2:
            raise ValueError("Exit error, invalid coordinates")
        if (
           self.entry[0] < 0 or self.entry[0] >= self.width or
           self.entry[1] < 0 or self.entry[1] >= self.height):
            raise ValueError("Entry error, invalid coordinates")
        if (
           self.exit[0] < 0 or self.exit[0] >= self.width or
           self.exit[1] < 0 or self.exit[1] >= self.height):
            raise ValueError("Exit error, invalid coordinates")

        if not re.fullmatch(r"[A-Za-z0-9_]+\.txt", self.output_file):
            raise ValueError(
                "OUTPUT_FILE must contain only letters, numbers, '_'"
                " and end with .txt"
            )
        return self


def get_config(filename: str) -> Config:
    """Retrieve the data from the indicated file.

    Retrieve every data, try to convert them into the correct type and
    send them in config_storage for further checking.

    Handle errors internally, raise them then terminate the program.

    Return dict with all the data ready to use

    Use:
        config = get_config("filename.txt")
    """
    config = Config()
    try:
        with open(filename, "r") as a:
            for line in a:
                line = line.strip()
                if not line:
                    continue
                key, value = line.split("=")

                if key in {"WIDTH", "HEIGHT"}:
                    if value.isdigit():
                        if key == "HEIGHT":
                            config.height = int(value)
                        else:
                            config.width = int(value)
                    else:
                        raise ValueError("Size error, invalid input")

                if key in {"ENTRY", "EXIT"}:
                    if "," in value:
                        parts = value.split(",")
                        if len(parts) != 2:
                            raise ValueError("Entry or Exit error, invalid"
                                             " coordinates.\nExemple: 5,8")
                        if parts[0].isdigit() and parts[1].isdigit():
                            if key == "ENTRY":
                                config.entry = [int(parts[0]), int(parts[1])]
                            else:
                                config.exit = [int(parts[0]), int(parts[1])]
                        else:
                            raise ValueError("Entry or Exit error, invalid"
                                             " coordinates.\nExemple: 5,8")
                    else:
                        raise ValueError("Entry or Exit error, invalid "
                                         "coordinates.\nExemple: 5,8")

                if key == "OUTPUT_FILE":
                    if not value.endswith(".txt"):
                        raise ValueError("OUTPUT_FILE error, invalid name")

                if key == "PERFECT":
                    if value == "True":
                        config.perfect = True
                    elif value == "False":
                        config.perfect = False
                    else:
                        raise ValueError("Type error, what kind of maze do you"
                                         " want?")

                if key == "SEED":
                    if value == "True":
                        config.seed = True
                    elif value == "False":
                        config.seed = False

        try:
            tester = config_storage(width=config.width,
                                    height=config.height,
                                    entry=config.entry,
                                    exit=config.exit,
                                    output_file=config.output_file,
                                    perfect=config.perfect)
        except ValidationError as err:
            for e in err.errors():
                print(e["msg"])
            sys.exit()
        tester = tester
    except FileNotFoundError:
        print("File not found")
        sys.exit()
    except PermissionError:
        print("No permission")
        sys.exit()
    except ValueError:
        print("Invalid data type")
        sys.exit()
    return config


# def main() -> None:
#     print("")
#     a = get_config("config.txt")
#     print(a)
#     width = a.width
#     height = a.height
#     entry = a.entry
#     exit = a.exit
#     output_file = a.output_file
#     perfect = a.perfect
#     seed = a.seed
#     print("")
#     print(width, height, entry, exit, output_file, perfect, seed)


# if __name__ == "__main__":
#     main()


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def wall_breaker(maze: list[list[Cell]], x: int, y: int, wall: str) -> None:
    """Break the selected wall between two adjacent cells.

    Take the selected wall, open it, go to the adjacent cell,
    open the corresponding wall, mark both as visited.
    """
    if wall == "north":
        maze[y][x].north = bool(0)
        maze[y][x].is_visited = True
        maze[y - 1][x].south = bool(0)
        maze[y - 1][x].is_visited = True
    if wall == "east":
        maze[y][x].east = bool(0)
        maze[y][x].is_visited = True
        maze[y][x + 1].west = bool(0)
        maze[y][x + 1].is_visited = True
    if wall == "south":
        maze[y][x].south = bool(0)
        maze[y][x].is_visited = True
        maze[y + 1][x].north = bool(0)
        maze[y + 1][x].is_visited = True
    if wall == "west":
        maze[y][x].west = bool(0)
        maze[y][x].is_visited = True
        maze[y][x - 1].east = bool(0)
        maze[y][x - 1].is_visited = True


def way_maker(maze: list[list[Cell]], data: Config,
              x: int, y: int) -> list[int]:
    """Select and open the next path in the maze.

    Determine which walls can be broken, randomly select one,
    open the corresponding passage, and return the coordinates
    of the next cell to explore.

    Raises:
        ValueError: If the maze becomes unsolvable.
    """
    # List the breakables walls.
    directions = []
    # print(len(maze[y]))  # ****
    if y != 0 and maze[y - 1][x].is_ft != 1 and maze[y - 1][x].is_visited != 1:
        directions.append("north")
    if (x < (data.width - 1) and maze[y][x + 1].is_ft != 1 and
            maze[y][x + 1].is_visited != 1):
        directions.append("east")
    if (y < (data.height - 1) and maze[y + 1][x].is_ft != 1 and
            maze[y + 1][x].is_visited != 1):
        directions.append("south")
    if x != 0 and maze[y][x - 1].is_ft != 1 and maze[y][x - 1].is_visited != 1:
        directions.append("west")

    # Security for unsolvable maze.
    try:
        if len(directions) == 0 and maze[y][x].is_start:
            raise ValueError("Error, unsolvable maze")
    except ValueError as err:
        print(err)
        sys.exit()

    # If no wall can be broken return the actual position.
    if len(directions) == 0:
        return [x, y]

    # Take the list of breakable walls, chose one, send it to the breaking.
    chosen: str = random.choice(directions)
    wall_breaker(maze, x, y, chosen)

    # Return the new adress.
    if chosen == "north":
        return [x, y - 1]
    if chosen == "east":
        return [x + 1, y]
    if chosen == "south":
        return [x, y + 1]
    if chosen == "west":
        return [x - 1, y]
    return []


def maze_checker(maze: list[list[Cell]],
                 data: Config) -> int:  # , path[-1][0], path[-1][1] ****
    """Check for any unopened cell, can return the total."""
    total: int = 0
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            # print("x =", x, "y =", y)  # ****
            # print("WIDTH HEIGHT", data["WIDTH"], data["HEIGHT"])
            if maze[y][x].is_visited == 0:
                total += 1
    return int(total)


# **** faire en sort que si il tombe sur exit il revienne en arriere
def wanderer(maze: list[list[Cell]], loc: list[int],
             data: Config) -> None:
    """Explore the maze and create valid paths.

    Move through the maze while opening walls between cells.
    Store visited coordinates to allow rollback when reaching
    dead ends. Mark the correct path when generating a perfect
    maze.
    """
    path: list[list[int]] = [loc]
    path_found: bool = False

    while maze_checker(maze, data):  # , path[-1][0], path[-1][1] ****
        try:
            new_loc: list[int] = way_maker(maze, data,
                                           path[-1][0], path[-1][1])
        except ValueError as err:
            print(err)
            sys.exit()

        # Create the perfect way, only for perfect path.
        if (
           maze[new_loc[1]][new_loc[0]].is_exit
           and data.perfect and path_found == 0):
            ariane_string(maze, path, data)
            data.path = path.copy()
            data.path.append(new_loc)
            path_found == 1

        # Roll back if exit is found.
        if maze[new_loc[1]][new_loc[0]].is_exit:
            path.pop()

        # If wanderer did not move, it is stuck, so it remove the last.
        # position and restart from the new last location on the list.
        # print("MAZE LOC", maze[new_loc[1]][new_loc[0]].is_exit)  # ****
        if not maze[new_loc[1]][new_loc[0]].is_exit:
            # print("backtrack")  # ****
            if new_loc == path[-1]:
                path.pop()
            else:
                path.append(new_loc)


# def main() -> None:
#     from maze_map import maze_creator
#     from get_config import get_config
#     from role_atribution import atributor_exit, atributor_start, fourtier

#     data = get_config("config.txt")
#     maze = maze_creator(data.height, data.width)

#     fourtier(maze, data.height, data.width)
#     atributor_start(maze, data.entry)
#     atributor_exit(maze, data.exit)
#     print("END REACHED")


# if __name__ == "__main__":
#     main()


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def atributor_start(maze: list[list[Cell]], start: list[int]) -> None:
    """Create the entry"""
    maze[(start[1])][(start[0])].is_start = True
    maze[(start[1])][(start[0])].is_way_out = True


def atributor_exit(maze: list[list[Cell]], exit: list[int]) -> None:
    """Create the exit and check overlapping with the entry"""
    try:
        maze[exit[1]][exit[0]].is_exit = True
        maze[exit[1]][exit[0]].is_way_out = True
        if maze[exit[1]][exit[0]].is_start:
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
                # **** may cause a mypy error later
                maze[start_v + x][start_o + y].is_ft = bool(int(logo[x][y]))
                maze[start_v + x][start_o + y].is_visited = bool(
                    int(logo[x][y]))
    except ValueError as err:
        print(err)
        sys.exit()


def ariane_string(maze: list[list[Cell]], the_way: list[list[int]],
                  config: Config):
    """Create the exit way

    Take the list of coordinates leading to the exit and change the atribute
    is_way_out"""
    for x, y in the_way:
        maze[y][x].is_way_out = True


# ****
"""def direction_instruction(Config: Config) -> str:
    path_instructions: str = ""

    for x in range(len(Config.path) - 1):
        if path_instructions[x][0] > path_instructions[x + 1][0]:
            path_instructions += "E"
        if path_instructions[x][0] > path_instructions[x - 1][0]:
            path_instructions += "W"
        if path_instructions[x][1] > path_instructions[x + 1][1]:
            path_instructions += "S"
        if path_instructions[x][1] > path_instructions[x - 1][1]:
            path_instructions += "N"

    return path_instructions"""


# def main() -> None:
#     from get_config import get_config
#     a = get_config("config.txt")
#     a = a
#     width = 12
#     height = 12
#     start = [1, 2]
#     exit = [9, 10]

#     maze = maze_creator(height, width)
#     fourtier(maze, height, width)
#     atributor_start(maze, start)
#     atributor_exit(maze, exit)

#     for x in range(height):
#         for y in range(width):
#             if maze[x][y].is_ft == 1:
#                 print("XXXX", sep="", end="")
#             else:
#                 print(maze[x][y].upper_closed, sep="", end="")
#         print("o\n", end="")

#         for y in range(width):
#             if maze[x][y].is_ft == 1:
#                 print("0000", sep="", end="")
#             elif maze[x][y].is_start == 1:
#                 print("0SSS", sep="", end="")
#             elif maze[x][y].is_exit == 1:
#                 print("0EEE", sep="", end="")
#             else:
#                 print(maze[x][y].left_closed, sep="", end="")
#         print("0\n", end="")

#     print("oooo" * width, "o\n", sep="", end="")

#     print("Hexa =", maze[0][0].get_hexa())
#     print("Total wall =", maze[0][0].get_wallnumber())


# if __name__ == "__main__":
#     main()


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def coords_to_direction(path: List[list[int]]) -> str:
    directions = []

    for i in range(1, len(path)):
        x1, y1 = path[i - 1]
        x2, y2 = path[i]

        if x2 == x1 - 1:
            directions.append("W")
        elif x2 == x1 + 1:
            directions.append("E")
        elif y2 == y1 - 1:
            directions.append("N")
        elif y2 == y1 + 1:
            directions.append("S")

    return "".join(directions)


def generate_output_file(
    filename: str,
    maze: list[list[Cell]],  # la map de maze_map
    entry: list[int],
    exit: list[int],
    solution_path: list[list[int]]
) -> None:

    with open(filename, "w") as f:
        for row in maze:
            # conversion en hexa par cellule pour chaque ligne
            line = "".join(cell.get_hexa() for cell in row)
            f.write(line + "\n")

        f.write(f"\n{entry[0]},{entry[1]}\n")

        f.write(f"{exit[0]},{exit[1]}\n")

        # conversion du path en N-S-E-W
        f.write(coords_to_direction(solution_path) + "\n")


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# break the wall semi randomly to make it imperfect
# It works
def imperfect_maker(maze: list[list[Cell]],
                    data: Config):
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x].get_wallnumber() > 2:
                directions = []
                if y != 0 and maze[y - 1][x].is_ft != 1 and maze[y][x].north:
                    directions.append("north")
                if (
                    x < (data.width - 1) and maze[y][x + 1].is_ft != 1
                ) and maze[y][x].east:
                    directions.append("east")
                if (
                    y < (data.height - 1) and maze[y + 1][x].is_ft != 1
                ) and maze[y][x].south:
                    directions.append("south")
                if x != 0 and maze[y][x - 1].is_ft != 1 and maze[y][x].west:
                    directions.append("west")
                if len(directions):
                    chosen: str = random.choice(directions)
                    wall_breaker(maze, x, y, chosen)

            if maze[y][x].get_wallnumber() == 2:
                directionss = []
                if y != 0 and maze[y - 1][x].is_ft != 1 and maze[y][x].north:
                    directionss.append("north")
                if (
                    x < (data.width - 1) and maze[y][x + 1].is_ft != 1
                ) and maze[y][x].east:
                    directionss.append("east")
                if (
                    y < (data.width - 1) and maze[y + 1][x].is_ft != 1
                ) and maze[y][x].south:
                    directionss.append("south")
                if x != 0 and maze[y][x - 1].is_ft != 1 and maze[y][x].west:
                    directionss.append("west")

                # Protection to avoid crash at angles
                if len(directionss):
                    chosen2: str = random.choice(directionss)
                    if random.randrange(0, 4) == 0:
                        wall_breaker(maze, x, y, chosen2)


# Filter the breakable wall
def open_door(maze: list[list[Cell]],
              data: Config, x: int, y: int):
    directions = []
    if y >= 1 and maze[y - 1][x].is_ft != 1 and maze[y - 1][x].is_visited != 1\
            and maze[y][x].north != 1:
        directions.append("north")
        maze[y - 1][x].is_visited = True
    if (x < (data.width - 1) and maze[y][x + 1].is_ft != 1 and
            maze[y][x + 1].is_visited != 1) and maze[y][x].east != 1:
        directions.append("east")
        maze[y][x + 1].is_visited = True
    if (y < (data.height - 1) and maze[y + 1][x].is_ft != 1 and
            maze[y + 1][x].is_visited != 1) and maze[y][x].south != 1:
        directions.append("south")
        maze[y + 1][x].is_visited = True
    if x >= 1 and maze[y][x - 1].is_ft != 1 and maze[y][x - 1].is_visited != 1\
            and maze[y][x].west != 1:
        directions.append("west")
        maze[y][x - 1].is_visited = True
    if maze[y][x].is_start == 1:
        print(directions)
    return directions


# refaire de zero
# faire un systeme avec une liste de sauvegarde, une liste en cours
# d usage et une liste a rajouter?
def imperfect_solver(maze: list[list[Cell]], data: Config):
    path_found: bool = False
    # reset the visited status
    for a in range(data.height):
        for b in range(data.width):
            if not maze[a][b].is_ft:
                maze[a][b].is_visited = False

    # list all the diferent ways
    work_flow: list[list[list[int]]] = [[list(data.entry)]]

    # set entry as visited
    maze[data.entry[1]][data.entry[0]].is_visited = True

    # Utilise direction comme un compteur, je le vide pour eviter d allonger
    # en boucle le meme lot de cheminsd.
    # Si j ajoute NSE, alors ca vas creer les chemins SE et il vas attaquer le
    # chemin S au coup suivant,
    # Je veut eviter ca pour ne pas avoir une meduse mono directionnelle qui
    # englobe tout en forme d escargot
    # continue until exit is set a visited
    while maze[data.exit[1]][data.exit[0]].is_visited == 0:
        new_branch: list[list[list[int]]] = []
        for c in work_flow:  # cycle through all the ways
            directions: list[str] = []  # stock the possible forks
            if len(directions):  # Empty the previous forks and cycle to avoid
                # following the same group of forks *** may actually be useless
                directions.pop()
                continue
            # print("HERE", c)  # ****
            # list all the forks
            directions = open_door(maze, data, c[-1][0], c[-1][1])
            if not directions:
                continue

            # print(c)  # ****
            # print("Direction", directions)
            # create the new list while adding the directions
            while len(directions):
                # print("here z")  # ****
                new_way: list[list[int]] = [p[:] for p in c]
                if directions[-1] == "north":
                    maze[new_way[-1][1] - 1][new_way[-1][0]].is_visited = True
                    new_way.append([new_way[-1][0], new_way[-1][1] - 1])
                if directions[-1] == "east":
                    maze[new_way[-1][1]][new_way[-1][0] + 1].is_visited = True
                    new_way.append([new_way[-1][0] + 1, new_way[-1][1]])
                if directions[-1] == "south":
                    maze[new_way[-1][1] + 1][new_way[-1][0]].is_visited = True
                    new_way.append([new_way[-1][0], new_way[-1][1] + 1])
                if directions[-1] == "west":
                    maze[new_way[-1][1]][new_way[-1][0] - 1].is_visited = True
                    new_way.append([new_way[-1][0] - 1, new_way[-1][1]])
                new_branch.append(new_way)
                directions.pop()

        while len(work_flow):
            work_flow.pop()
        while len(new_branch):
            # print("ddddddddddddddddddddddddddddddddddddddddddddd")  # ****
            work_flow.append(new_branch[-1])
            new_branch.pop()
            # optimisation possible: si aucun chemin dispo et pas sur exit:
            # efface le chemin. Ca permet de trier les dead end pour
            # economiser des passages
        for c in work_flow:
            # print("YYYYYYYYYYY")  # ****
            # print(c[-1][1], c[-1][0], "HHHHHHHHHHHHHHHHHHH")  # ****
            if maze[c[-1][1]][c[-1][0]].is_exit and path_found == 0:
                maze[c[-1][1]][c[-1][0]].is_visited = True
                ariane_string(maze, c, data)
                data.path = c.copy()
                # data.path.append([c[-1][1]], [c[-1][0]])
                path_found == 1


"""
def way_maker(maze: list[list[Cell]], data: dict[str, bool | str | int | list],
              x: int, y: int) -> list[int]:
    # List the breakables walls.
    directions = []
    if y != 0 and maze[y - 1][x].is_ft != 1 and maze[y - 1][x].is_visited != 1:
        directions.append("north")
    if (x < (data["WIDTH"] - 1) and maze[y][x + 1].is_ft != 1 and
            maze[y][x + 1].is_visited != 1):
        directions.append("east")
    if (y < (data["HEIGHT"] - 1) and maze[y + 1][x].is_ft != 1 and
            maze[y + 1][x].is_visited != 1):
        directions.append("south")
    if x != 0 and maze[y][x - 1].is_ft != 1 and maze[y][x - 1].is_visited != 1:
        directions.append("west")

    # Security for unsolvable maze.
    try:
        if len(directions) == 0 and maze[y][x].is_start:
            raise ValueError("Error, unsolvable maze")
    except ValueError as err:
        print(err)
        sys.exit()

    # If no wall can be broken return the actual position.
    if len(directions) == 0:
        return [x, y]

    # Take the list of breakable walls, chose one, send it to the breaking.
    chosen: str = random.choice(directions)
    print(chosen)  # ****
    wall_breaker(maze, x, y, chosen)

    # Return the new adress.
    if chosen == "north":
        return [x, y - 1]
    if chosen == "east":
        return [x + 1, y]
    if chosen == "south":
        return [x, y + 1]
    if chosen == "west":
        return [x - 1, y]
"""

# if __name__ == "__main__":
#     main()

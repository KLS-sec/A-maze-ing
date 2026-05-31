import random
import sys
from config_parsing import Config
from dataclasses import dataclass


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
        elif self.is_way_out == 1 and maze[y - 1][x].is_way_out == 1:
            # add the conditionnal to trigger the coloration
            if show_path:
                upper_wall["upper_is_way_out"] = self.upper_is_way_out
            else:
                upper_wall["upper_is_way_out"] = "   "
        # normal
        else:
            upper_wall["upper_open"] = self.upper_open

        return upper_wall

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


def maze_checker(maze: list[list[Cell]]) -> int:
    """Check for any unopened cell, can return the total."""
    total: int = 0
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x].is_visited == 0:
                total += 1
    return int(total)


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

    while maze_checker(maze):
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
            ariane_string(maze, path)
            data.path = path.copy()
            data.path.append(new_loc)
            path_found = True

        # Roll back if exit is found.
        if maze[new_loc[1]][new_loc[0]].is_exit:
            path.pop()

        # If wanderer did not move, it is stuck, so it remove the last.
        # position and restart from the new last location on the list.
        if not maze[new_loc[1]][new_loc[0]].is_exit:
            if new_loc == path[-1]:
                path.pop()
            else:
                path.append(new_loc)


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
                maze[start_v + x][start_o + y].is_ft = bool(int(logo[x][y]))
                maze[start_v + x][start_o + y].is_visited = bool(
                    int(logo[x][y]))
    except ValueError as err:
        print(err)
        sys.exit()


def ariane_string(maze: list[list[Cell]], the_way: list[list[int]]):
    """Create the exit way

    Take the list of coordinates leading to the exit and change the atribute
    is_way_out"""
    for x, y in the_way:
        maze[y][x].is_way_out = True


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
            # list all the forks
            directions = open_door(maze, data, c[-1][0], c[-1][1])
            if not directions:
                continue

            # print("Direction", directions)
            # create the new list while adding the directions
            while len(directions):
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
            work_flow.append(new_branch[-1])
            new_branch.pop()
            # optimisation possible: si aucun chemin dispo et pas sur exit:
            # efface le chemin. Ca permet de trier les dead end pour
            # economiser des passages
        for c in work_flow:
            if maze[c[-1][1]][c[-1][0]].is_exit and path_found == 0:
                maze[c[-1][1]][c[-1][0]].is_visited = True
                ariane_string(maze, c)
                data.path = c.copy()
                # data.path.append([c[-1][1]], [c[-1][0]])
                path_found = True


class MazeGenerator:
    def __init__(self, config: Config):
        self.config = config

    def generate(self) -> list[list[Cell]]:
        return maze_creator(self.config.height, self.config.width)

    def solve(self, genmaze: list[list[Cell]]) -> list[list[Cell]]:
        if self.config.width > 11 and self.config.height > 9:
            fourtier(genmaze, self.config.height, self.config.width)
        atributor_start(genmaze, self.config.entry)
        atributor_exit(genmaze, self.config.exit)
        wanderer(genmaze, self.config.entry, self.config)
        if not self.config.perfect:
            imperfect_maker(genmaze, self.config)
            imperfect_solver(genmaze, self.config)
        return genmaze

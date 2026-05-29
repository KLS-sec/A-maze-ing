#!/usr/bin/env python3

import random
from maze_map import Cell
from get_config import Config
from role_atribution import ariane_string
import sys


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


def maze_checker(maze: list[list[Cell]],
                 data: Config,
                 x: int, y: int) -> int:
    """Check for any unopened cell, can return the total."""
    total: int = 0
    for y in range(data.height):
        for x in range(data.width):
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

    while maze_checker(maze, data, path[-1][0], path[-1][1]):
        try:
            new_loc: list[int] = way_maker(maze, data,
                                           path[-1][0], path[-1][1])
        except ValueError as err:
            print(err)
            sys.exit()

        # Create the perfect way, only for perfect path.
        if maze[new_loc[1]][new_loc[0]].is_exit and data.perfect:
            ariane_string(maze, path, data)

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


def main() -> None:
    from maze_map import maze_creator
    from get_config import get_config
    from role_atribution import atributor_exit, atributor_start, fourtier

    data = get_config("config.txt")
    maze = maze_creator(data.height, data.width)

    fourtier(maze, data.height, data.width)
    atributor_start(maze, data.entry)
    atributor_exit(maze, data.exit)
    print("END REACHED")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import random
from maze_map import Cell
from role_atribution import ariane_string


# toujours bien verifier qu il n y a pas inversion y - x, Y en premier

# break the selected wall in the selected cell, then break the adjacent one
def wall_breaker(map: list[list[Cell]], x: int, y: int, wall: str):
    if wall == "north":
        map[y][x].north = bool(0)
        map[y - 1][x].south = bool(0)
    if wall == "east":
        map[y][x].east = bool(0)
        map[y][x + 1].west = bool(0)
    if wall == "south":
        map[y][x].south = bool(0)
        map[y + 1][x].north = bool(0)
    if wall == "west":
        map[y][x].west = bool(0)
        map[y][x - 1].east = bool(0)

# randomly select the wall to break
# give it to wall breaker
# return the new adress
def way_maker(map: list[list[Cell]], data: dict[str, bool | str | int | list], x: int, y: int):
    if map[y][x].is_exit:
        return list(x, y)

    # list the breakables walls
    directions = []
    if y != 0 and map[y - 1][x].is_ft != 1 and map[y - 1][x].is_visited != 1:
        directions.append("north")
    if x != (data["WIDTH"] + 1) and map[y][x + 1].is_ft != 1 and map[y][x + 1].is_visited != 1:
        directions.append("east")
    if y != (data["HEIGHT"] + 1) and map[y + 1][x].is_ft != 1 and map[y + 1][x].is_visited != 1:
        directions.append("south")
    if x != 0 and map[y][x - 1].is_ft != 1 and map[y][x - 1].is_visited != 1:
        directions.append("west")

    # take the list of breakable walls, chose one, send it to the breaking
    chosen: str = random.choice(directions)
    wall_breaker(map, x, y, chosen)

    # return the new adress
    if chosen == "north":
        return list(x, y + 1)
    if chosen == "east":
        return list(x + 1, y)
    if chosen == "south":
        return list(x, y - 1)
    if chosen == "west":
        return list(x - 1, y)
    return list(x, y)

# check if there are still any unopened cell
# can return the total, seless now, made just in case
def map_checker(map: list[list[Cell]], data: dict[str, bool | str | int | list], x: int, y: int) -> int:
    total = 0
    for x in range(data["HEIGHT"]):
        for y in range(data["WIDTH"]):
            if map[y][x].is_visited == 0:
                total += 1
    return total


# this agent take the starting point
# call way_maker to explore, and find a new path
# localisation keep track of the way
# if the path is blocked it goes back one step
# if it find exit and maze is perfect it convert the_way with ariane_string
def wanderer(map: list[list[Cell]], loc: list[int], data: dict[str, bool | str | int | list], x: int, y: int):
    path: list[list[int]] = [loc]

    # check if the map still need to be explored
    while map_checker(map, data, path[-1][0], path[-1][1]):
        # give the actual location, open the wall, receive the new location
        new_loc: list[int] = way_maker(map, data, path[-1][0], path[-1][1])

        # if wanderer did not move it is stuck, remove last position and restart
        if new_loc == path[-1]:
            path.pop()
        else:
            path.append(new_loc)

        # create the perfect way **** only for perfect path
        if map[new_loc[0]][new_loc[1]].is_exit and data["PERFECT"]:
            the_way = path  # **** create a storage for the correct way?
            ariane_string(map, the_way)


"""
@dataclass
class Cell:
    is_ft: bool = 0
    is_start: bool = 0
    is_exit: bool = 0
    is_way_out: bool = 0  # is it the perfect way start - exit
    visited: bool = 0

    north: bool = 1
    east: bool = 1
    south: bool = 1
    west: bool = 1

    def __post_init__(self):  # will initiate these value after initialisation
        self.hexa = (self.north * 1 + self.east * 2 + self.south * 4 +
                     self.west * 8)
        self.total_wall = (self.north + self.east + self.south + self.west)

    upper_closed: str = "oooo"
    upper_open: str = "o   "
    middle_closed: str = "0   "
    middle_open: str = "    "
"""


def main() -> None:
    from maze_map import map_creator
    from get_config import get_config
    from role_atribution import atributor_exit, atributor_start, fourtier

    data = get_config("config.txt")
    map = map_creator(data["HEIGHT"], data["WIDTH"])

    map = fourtier(map, data["HEIGHT"], data["WIDTH"])
    map = atributor_start(map, data["ENTRY"])
    map = atributor_exit(map, data["EXIT"])


if __name__ == "__main__":
    main()

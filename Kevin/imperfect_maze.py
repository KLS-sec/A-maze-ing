#!/usr/bin/env python3

from maze_map import Cell
import way_maker
import random

# break the wall semi randomly to make it imperfect
def imperfect_maker(maze: list[list[Cell]], data: dict[str, bool | str | int | list]):
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x].get_wallnumber() > 2:
                directions = []
                if y != 0 and maze[y - 1][x].is_ft != 1 and maze[y][x].north:
                    directions.append("north")
                if (x < (data["WIDTH"] - 1) and maze[y][x + 1].is_ft != 1) and maze[y][x].east:
                    directions.append("east")
                if (y < (data["HEIGHT"] - 1) and maze[y + 1][x].is_ft != 1) and maze[y][x].south:
                    directions.append("south")
                if x != 0 and maze[y][x - 1].is_ft != 1 and maze[y][x].west:
                    directions.append("west")
                if len(directions):
                    chosen: str = random.choice(directions)
                    way_maker.wall_breaker(maze, x, y, chosen)

            if maze[y][x].get_wallnumber() == 2:
                directionss = []
                if y != 0 and maze[y - 1][x].is_ft != 1 and maze[y][x].north:
                    directionss.append("north")
                if (x < (data["WIDTH"] - 1) and maze[y][x + 1].is_ft != 1) and maze[y][x].east:
                    directionss.append("east")
                if (y < (data["HEIGHT"] - 1) and maze[y + 1][x].is_ft != 1) and maze[y][x].south:
                    directionss.append("south")
                if x != 0 and maze[y][x - 1].is_ft != 1 and maze[y][x].west:
                    directionss.append("west")

                # Protection to avoid crash at angles
                if len(directionss):
                    chosen: str = random.choice(directionss)
                    if random.randrange(0, 3) == 0:
                        way_maker.wall_breaker(maze, x, y, chosen)


# Filter the breakable wall
def water_dam(maze: list[list[Cell]], data: dict[str, bool | str | int | list], x: int, y: int):
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
    return directions


def imperfect_solver(maze: list[list[Cell]], data: dict[str, bool | str | int | list]):
    x = data["ENTRY"][0]
    y = data["ENTRY"][1]

    # list all the diferent ways
    water_flow: list[list[list[int]]] = [[list[data["ENTRY"]]]]

    # reset the visited status
    for a in range(data["HEIGHT"]):
        for b in range(data["WIDTH"]):
            if not maze[a][b].is_ft:
                maze[a][b].is_visited == 0

    # Utilise direction comme un compteur, je le vide pour eviter d allonger en boucle le meme lot de cheminsd
    # Si j ajoute NSE, alors ca vas creer les chemins SE et il vas attaquer le chemin S au coup suivant,
    # Je veut eviter ca pour ne pas avoir une meduse mono directionnelle qui englobe tout en forme d escargot
    directions = []  # stock the possible forks
    while maze[data["EXIT"][1]][data["EXIT"][0]].is_visited == 0:  # continue until exit is set a visited
        for c in water_flow:  # cycle through all the ways
            if len(directions):  # Empty the previous forks and cycle to avoir following the same group of forks
                directions.pop()
                continue
            directions = water_dam(maze, data, water_flow[c][-1][0], water_flow[c][-1][1])  # list all the forks
            # add the first fork to the list in use
            if len(directions):
                new_way = c  # used for the next step, not this one
                if directions == "north":
                    c.append([x, y - 1])
                if directions == "east":
                    c.append([x + 1, y])
                if directions == "south":
                    c.append([x, y + 1])
                if directions == "west":
                    c.append([x - 1, y])
                directions.pop()

            # if more create new list
            if len(directions):
                if directions == "north":
                    c.append([x, y - 1])
                if directions == "east":
                    c.append([x + 1, y])
                if directions == "south":
                    c.append([x, y + 1])
                if directions == "west":
                    c.append([x - 1, y])

            # do not empty the list except for the first element
            # optimisation possible: si aucun chemin dispo et pas sur exit: efface le chemin. Ca permet de trier les dead end pour economiser des passages


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

if __name__ == "__main__":
    main()

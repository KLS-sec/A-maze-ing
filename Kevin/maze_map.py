#!/usr/bin/env python3

# here I CONSTRUC the cells and the map
# modification and use will be somewhere else
from dataclasses import dataclass


@dataclass
class Cell:
    is_ft: bool = 0
    is_start: bool = 0
    is_exit: bool = 0
    is_way_out: bool = 0  # is it the perfect way start - exit
    is_visited: bool = 0

    north: bool = 1
    east: bool = 1
    south: bool = 1
    west: bool = 1

    # **** a modifier, faire des fonction get_hexa et get_total sinon ca ne se recalculera jamais

    # **** ajouter des condition pour savoir quoi print, au lieu de juste print
    # un element, on call une fonction qui verifie ses propre condition et return la bonne chose a print
    # exemple: print(wall()) => def wall if 42 = 1 return y, if exit = 1 return y etc

    def __post_init__(self):  # will initiate these value after initialisation
        self.hexa = (self.north * 1 + self.east * 2 + self.south * 4 +
                     self.west * 8)
        self.total_wall = (self.north + self.east + self.south + self.west)

    upper_closed: str = "oooo"
    upper_open: str = "o   "
    middle_closed: str = "0   "
    middle_open: str = "    "


def map_creator(height: int, width: int) -> list[list[Cell]]:
    map = []
    for _ in range(height):
        row = []
        for _ in range(width):
            row.append(Cell())
        map.append(row)
    return map


def main() -> None:
    from get_config import get_config
    a = get_config("config.txt")
    width = 8
    height = a["HEIGHT"]

    map = map_creator(height, width)

    for x in range(height):
        for y in range(width):
            print(map[x][y].upper_closed, sep="", end="")
        print("o\n", end="")
        for y in range(width):
            print(map[x][y].middle_closed, sep="", end="")
        print("0\n", end="")

    print("oooo" * width, "o\n", sep="", end="")
    print("Hexa =", map[0][0].hexa)
    print("Total wall =", map[0][0].total_wall)


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

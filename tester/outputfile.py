from typing import List, Tuple
from maze_map import Cell


# conversion du path en N-S-E-W
def coords_to_direction(path: List[Tuple[int, int]]) -> str:
    directions = []

    for i in range(1, len(path)):
        x1, y1 = path[i - 1]
        x2, y2 = path[i]

        if x2 == x1 - 1:
            directions.append("N")
        elif x2 == x1 + 1:
            directions.append("S")
        elif y2 == y1 - 1:
            directions.append("W")
        elif y2 == y1 + 1:
            directions.append("E")

    return "".join(directions)


def generate_output_file(
    filename: str,
    maze: list[list[Cell]],  # la map de maze_map
    entry: tuple[int, int],
    exit: tuple[int, int],
    solution_path: list[tuple[int, int]]  # a changer si c'est pas comme ca: [(0,0), (0,1), (0,2), (1,2), (2,2), (2,3)]
) -> None:

    with open(filename, "w") as f:
        f.write("=== A-Maze-ing Output File ===\n\n")

        f.write("[MAZE]\n")
        for row in maze:
            # conversion en hexa par cellule pour chaque ligne ("X" = maj "x" = min)
            line = "".join(format(Cell.get_hexa, "X") for cell in row)
            f.write(line + "\n")

        f.write("[ENTRY]\n")
        f.write(f"x={entry[0]}\n")
        f.write(f"y={entry[1]}\n\n")

        f.write("[EXIT]\n")
        f.write(f"x={exit[0]}\n")
        f.write(f"y={exit[1]}\n\n")

        f.write("\n[SOLUTION]\n")
        # conversion du path en N-S-E-W
        f.write(coords_to_direction(solution_path) + "\n")
        f.write("\n[END]\n")

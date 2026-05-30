from typing import List, Tuple
from maze_map import Cell


# conversion du path en N-S-E-W
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
    solution_path: list[list[int]]  # a changer si c'est pas comme ca: [(0,0), (0,1), (0,2), (1,2), (2,2), (2,3)]
) -> None:

    with open(filename, "w") as f:
        for row in maze:
            # conversion en hexa par cellule pour chaque ligne ("X" = maj "x" = min)
            line = "".join(str(cell.get_hexa()) for cell in row)
            f.write(line + "\n")

        f.write(f"\n{entry[0]},{entry[1]}\n")

        f.write(f"{exit[0]},{exit[1]}\n")

        # conversion du path en N-S-E-W
        f.write(coords_to_direction(solution_path) + "\n")

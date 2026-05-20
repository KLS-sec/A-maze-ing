from random import choice, seed
from typing import Any
import os


class Cell():
    def __init__(self, cell_x: int, cell_y: int,
                 maze_x: int, maze_y: int) -> None:

        self.cell_x: int = cell_x
        self.cell_y: int = cell_y

        self.maze_x: int = maze_x
        self.maze_y: int = maze_y

        self.wall_stat: list[str] = ['1', '1', '1', '1']  # N, E, S, W
        self.is_visited: bool = True
        self.path: bool = False

        self.a_way_out: bool = False
        self.nextway: list[str] = ['0', '0', '0', '0']

        self.is_exit: bool = False
        self.is_entry: bool = False

        self.isfortytwo: bool = False


class Wall():
    def __init__(self, maze_x: int, maze_y: int) -> None:

        self.maze_x: int = maze_x
        self.maze_y: int = maze_y

        self.path: bool = False
        self.next: list[str] = ['1', '1', '1', '1']

        self.a_way_out: bool = False
        self.nextway: list[str] = ['0', '0', '0', '0']

        self.isfortytwo: bool = False


class Maze_Generator():
    def __init__(self, height: int, width: int, is_perfect: bool) -> None:
        self.height: int = height
        self.width: int = width
        self.display_path: bool = True
        self.list_y_x: list[list[Cell | Wall]] = list()
        self.list_x: list[Cell | Wall] = list()
        self.lab_color: str = ""
        self.fortytwo_color: str = ""
        self.is_perfect = is_perfect

    def init_maze(self) -> None:
        cell_x: int = 0
        cell_y: int = 0

        for y in range(self.height*2+1):

            for x in range(self.width*2+1):

                if x % 2 != 0 and y % 2 != 0:
                    self.list_x.append(Cell(cell_x, cell_y, x, y))
                    cell_x += 1

                else:
                    self.list_x.append(Wall(x, y))

            if cell_x >= self.width:
                cell_x = 0
                cell_y += 1

            self.list_y_x.append(self.list_x.copy())
            self.list_x.clear()

    def binary_update(self) -> None:
        for y in range(1, len(self.list_y_x), 2):
            for x in range(1, len(self.list_y_x[y]), 2):
                cell = self.list_y_x[y][x]
                if isinstance(cell, Cell):
                    # North
                    if y > 1 and self.list_y_x[y-1][x].path:
                        cell.wall_stat[0] = '0'
                    else:
                        cell.wall_stat[0] = '1'

                    # East
                    if (x + 1 < len(self.list_y_x[y])
                       and self.list_y_x[y][x+1].path):
                        cell.wall_stat[1] = '0'
                    else:
                        cell.wall_stat[1] = '1'

                    # South
                    if (y + 1 < len(self.list_y_x)
                       and self.list_y_x[y+1][x].path):
                        cell.wall_stat[2] = '0'
                    else:
                        cell.wall_stat[2] = '1'

                    # West
                    if x > 1 and self.list_y_x[y][x-1].path:
                        cell.wall_stat[3] = '0'
                    else:
                        cell.wall_stat[3] = '1'

    def perfect_false(self) -> None:
        if self.is_perfect:
            return

        for row in self.list_y_x[1:-1:2]:
            row_walls = [
                tile for tile in row[1:-1]
                if isinstance(tile, Wall)
                and not tile.path
                and not tile.isfortytwo
            ]
            if row_walls:
                choice(row_walls).path = True

    def iterative_backtracking(self, conf_seed: int | None = None) -> None:
        seed(conf_seed)
        for y in self.list_y_x:
            for item in y:

                if isinstance(item, Cell):
                    if item.isfortytwo is False:
                        item.is_visited = False

                elif isinstance(item, Wall):
                    item.path = False

        start_cell = self.list_y_x[1][1]

        if isinstance(start_cell, Cell):
            start_cell.is_visited = True

        stack = [start_cell]

        while stack:
            current = stack[-1]
            neighbors = []
            directions = [
                (-1, 0, -2, 0),  # NORTH
                (1, 0, 2, 0),    # SOUTH
                (0, 1, 0, 2),    # EAST
                (0, -1, 0, -2)   # WEST
            ]

            for dy_wall, dx_wall, dy_cell, dx_cell in directions:
                ny, nx = current.maze_y + dy_cell, current.maze_x + dx_cell

                if 0 < ny < self.height * 2 and 0 < nx < self.width * 2:
                    neighbor = self.list_y_x[ny][nx]
                    if isinstance(neighbor, Cell) and not neighbor.is_visited:
                        neighbors.append((neighbor, ny - dy_cell + dy_wall,
                                          nx - dx_cell + dx_wall))

            if neighbors:
                next_cell, wall_y, wall_x = choice(neighbors)
                wall_obj = self.list_y_x[wall_y][wall_x]
                if isinstance(wall_obj, Wall):
                    wall_obj.path = True
                next_cell.is_visited = True
                stack.append(next_cell)

            else:
                stack.pop()
        self.perfect_false()
        self.binary_update()

    def solve_bfs(self, start_coords: tuple[int, int],
                  end_coords: tuple[int, int]) -> str:
        for y in self.list_y_x:
            for x in y:

                if isinstance(x, Cell | Wall):
                    x.a_way_out = False

        start_y, start_x = start_coords[0] * 2 + 1, start_coords[1] * 2 + 1
        end_y, end_x = end_coords[0] * 2 + 1, end_coords[1] * 2 + 1
        start_point = self.list_y_x[start_y][start_x]
        end_point = self.list_y_x[end_y][end_x]

        if isinstance(start_point, Cell) and isinstance(end_point, Cell):
            start_point.is_entry = True
            end_point.is_exit = True

        parent = {}
        queue: list[Any] = [(start_y, start_x, [])]
        visited = set([(start_y, start_x)])

        while queue:
            y, x, path = queue.pop(0)

            if (y, x) == (end_y, end_x):
                for py, px in path + [(y, x)]:
                    item = self.list_y_x[py][px]
                    item.a_way_out = True
                break

            for dy, dx, way in [(0, 1, 'E'), (0, -1, 'W'),
                                (1, 0, 'S'), (-1, 0, 'N')]:
                ny, nx = y + dy, x + dx

                if (0 <= ny < len(self.list_y_x)
                   and 0 <= nx < len(self.list_y_x[0])):
                    target = self.list_y_x[ny][nx]

                    if ((ny, nx) not in visited
                       and (isinstance(target, Cell)
                            or (isinstance(target, Wall) and target.path))):
                        visited.add((ny, nx))
                        parent[(ny, nx)] = ((y, x), way)
                        queue.append((ny, nx, path + [(y, x)]))

        path_directions = ""
        current = (end_y, end_x)

        while current in parent:
            prev_pos, direction = parent[current]
            path_directions = direction + path_directions
            current = prev_pos

        self.binary_update()

        return path_directions

    def save_maze_to_file(self, filename: str, entry: tuple[int, int],
                          exit: tuple[int, int]) -> None:
        with open(filename, 'w') as f:
            for y in self.list_y_x:
                row = ""
                for x in y:
                    if isinstance(x, Cell):
                        hex_value = hex(int(''.join(x.wall_stat[::-1]), 2))[2:]
                        row += hex_value.capitalize()
                if row:
                    f.write(row + "\n")

            f.write("\n")

            f.write(f"{entry[0]},{entry[1]}\n")
            f.write(f"{exit[0]},{exit[1]}\n")

            path = self.solve_bfs(entry, exit)
            output = path[::2]
            f.write(output + "\n")

    def check_term_size(self) -> bool:
        columns, lines = os.get_terminal_size()

        if columns < (self.width + 1) * 6 or lines < self.height * 2:
            os.system('clear')
            print("Terminal size too small")
            return False

        return True

    def check_coordinates(self, entry: tuple[int, int],
                          exit: tuple[int, int]) -> None:

        cell_en = self.list_y_x[entry[0]*2+1][entry[1]*2+1]
        cell_ex = self.list_y_x[exit[0]*2+1][exit[1]*2+1]

        if cell_en.isfortytwo:
            if isinstance(cell_en, Cell):
                raise ValueError("Entry point cannot be inside"
                                 " the 42 pattern !")
        elif cell_ex.isfortytwo:
            if isinstance(cell_ex, Cell):
                raise ValueError("Exit point cannot be inside"
                                 " the 42 pattern !")

    def make_fortytwo(self) -> None:
        "Implement the 42 pattern"
        center_x: int = int(self.width)
        center_y: int = int(self.height)

        if center_x % 2 == 0:
            center_x += 1

        if center_y % 2 == 0:
            center_y += 1

        for a in range(1, 8):
            self.list_y_x[center_y][center_x+a].isfortytwo = True
            self.list_y_x[center_y][center_x-a].isfortytwo = True

            self.list_y_x[center_y+1][center_x+a].isfortytwo = True
            self.list_y_x[center_y+1][center_x-a].isfortytwo = True

            self.list_y_x[center_y-1][center_x+a].isfortytwo = True
            self.list_y_x[center_y-1][center_x-a].isfortytwo = True

            self.list_y_x[center_y+3][center_x+a].isfortytwo = True
            self.list_y_x[center_y+4][center_x+a].isfortytwo = True
            self.list_y_x[center_y+5][center_x+a].isfortytwo = True

            self.list_y_x[center_y-3][center_x+a].isfortytwo = True
            self.list_y_x[center_y-4][center_x+a].isfortytwo = True
            self.list_y_x[center_y-5][center_x+a].isfortytwo = True

        for a in range(1, 4):
            self.list_y_x[center_y+2][center_x-a].isfortytwo = True
            self.list_y_x[center_y+3][center_x-a].isfortytwo = True
            self.list_y_x[center_y+4][center_x-a].isfortytwo = True
            self.list_y_x[center_y+5][center_x-a].isfortytwo = True

            self.list_y_x[center_y+2][center_x+a].isfortytwo = True

        for a in range(5, 8):
            self.list_y_x[center_y-2][center_x-a].isfortytwo = True
            self.list_y_x[center_y-3][center_x-a].isfortytwo = True
            self.list_y_x[center_y-4][center_x-a].isfortytwo = True
            self.list_y_x[center_y-5][center_x-a].isfortytwo = True

            self.list_y_x[center_y-2][center_x+a].isfortytwo = True

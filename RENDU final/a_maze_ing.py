#!/usr/bin/env python3

"""Terminal interface and maze rendering utilities."""

from colorama import Fore, Style, init
import os
import sys
from maze_generator import generator
from maze_generator.generator import MazeGenerator
from config_parsing import get_config


# Automatically reset terminal colors after each print.
init(autoreset=True)


# Available color schemes for maze rendering.
COLOR_SCHEMES = [
    {
        "wall": Fore.WHITE,
        "start": Fore.BLUE,
        "exit": Fore.RED,
        "ft": Fore.MAGENTA,
        "path": Fore.GREEN,
    },
    {
        "wall": Fore.CYAN,
        "start": Fore.YELLOW,
        "exit": Fore.BLUE,
        "ft": Fore.GREEN,
        "path": Fore.RED,
    },
    {
        "wall": Fore.BLUE,
        "start": Fore.GREEN,
        "exit": Fore.MAGENTA,
        "ft": Fore.RED,
        "path": Fore.YELLOW,
    },
]


def get_colors(index: int) -> dict[str, str]:
    """Return the color scheme associated with the given index."""
    return COLOR_SCHEMES[index]


def rotate_colors(index: int) -> int:
    """Return the index of the next color scheme."""
    return (index + 1) % len(COLOR_SCHEMES)


def color_map(maze: list[list[generator.Cell]], height: int, width: int,
              color_ind: int, show_path: bool) -> None:
    """Display the maze using the selected color scheme."""
    colors = get_colors(color_ind)

    def colorize(key: str) -> str:
        """Return a color depending on the Cell"""
        if (
            key == "upper_is_ft"
            or key == "upper_left_is_ft"
            or key == "left_is_ft"
            or key == "center_is_ft"
        ):
            return colors["ft"]
        if key == "center_is_start":
            return colors["start"]
        if key == "center_is_exit":
            return colors["exit"]
        return colors["wall"]

    for y in range(height):
        # Render upper walls.
        for x in range(width):
            cell = maze[y][x]
            lst_walls: dict[str, str] = cell.get_upper_wall(
                maze, x, y, show_path)
            for keys in lst_walls.keys():
                if keys == "upper_is_way_out" and show_path:
                    print(colors["path"] + lst_walls[keys] + Style.RESET_ALL,
                          end="")
                else:
                    print(colorize(keys) + lst_walls[keys] + Style.RESET_ALL,
                          end="")

        print(colors["wall"] + "o" + Style.RESET_ALL)

        # Render left walls.
        for x in range(width):
            cell = maze[y][x]
            lst_walls = cell.get_left_wall(maze, x, y, show_path)

            for keys in lst_walls.keys():
                if (
                    (keys == "left_is_way_out" or
                     keys == "center_is_way_out") and show_path
                ):
                    print(colors["path"] + lst_walls[keys] + Style.RESET_ALL,
                          end="")
                else:
                    print(colorize(keys) + lst_walls[keys] + Style.RESET_ALL,
                          end="")
        print(colors["wall"] + "o" + Style.RESET_ALL)
    print(colors["wall"] + "oooo" * width + "o" + Style.RESET_ALL)


def render(maze: list[list[generator.Cell]], height: int, width: int,
           color_ind: int, show_path: bool) -> None:
    """Clear the terminal and display the maze."""

    if maze:
        os.system("cls" if os.name == "nt" else "clear")
        color_map(maze, height, width, color_ind, show_path)


def gen_maze(mazegen: MazeGenerator) -> list[list[generator.Cell]]:
    """Generate and solve a maze."""

    map = mazegen.generate()
    maze = mazegen.solve(map)

    return maze


def coords_to_direction(path: list[list[int]]) -> str:
    """Generate the solution path."""
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


def generate_output_file(filename: str, maze: list[list[generator.Cell]],
                         entry: list[int], exit: list[int],
                         solution_path: list[list[int]]) -> None:
    """Generate the output file for the tester."""
    with open(filename, "w") as f:
        for row in maze:
            # convert in hexa for Cell in the row
            line = "".join(cell.get_hexa() for cell in row)
            f.write(line + "\n")
        f.write(f"\n{entry[0]},{entry[1]}\n")
        f.write(f"{exit[0]},{exit[1]}\n")
        # convert path into cardinal points
        f.write(coords_to_direction(solution_path) + "\n")


def ui(filename: str) -> None:
    """Run the interactive terminal interface.

    Load the configuration, generate a maze, and provide controls for
    regenerating the maze, displaying the solution path, and rotating
    the available color schemes.
    """

    show_path = True
    color_ind = 0

    data = get_config(filename)
    map = MazeGenerator(data)
    mazegen = gen_maze(map)

    generate_output_file(
        data.output_file,
        mazegen,
        data.entry,
        data.exit,
        data.path,
    )

    render(
        mazegen,
        data.height,
        data.width,
        color_ind,
        show_path,
    )

    txt = (
        "=== a-maze-ing ===\n"
        "1. Re-generate a new maze\n"
        "2. Show/Hide path from entry to exit\n"
        "3. Rotate maze colors\n"
        "4. Quit"
    )

    print(txt)

    if data.width < 11 or data.height < 9:
        print('Maze size does not allow "42" logo')

    try:
        param = input("Choice? (1-4): ").strip()
        while param != "4":
            if param == "1":
                mazegen = gen_maze(map)
                generate_output_file(
                    data.output_file,
                    mazegen,
                    data.entry,
                    data.exit,
                    data.path,
                )
                render(
                    mazegen,
                    data.height,
                    data.width,
                    color_ind,
                    show_path,
                )
            elif param == "2":
                show_path = not show_path
                render(
                    mazegen,
                    data.height,
                    data.width,
                    color_ind,
                    show_path,
                )
            elif param == "3":
                color_ind = rotate_colors(color_ind)
                render(
                    mazegen,
                    data.height,
                    data.width,
                    color_ind,
                    show_path,
                )
            else:
                mazegen = gen_maze(map)
                generate_output_file(
                    data.output_file,
                    mazegen,
                    data.entry,
                    data.exit,
                    data.path,
                )
                render(
                    mazegen,
                    data.height,
                    data.width,
                    color_ind,
                    show_path,
                )
            print(txt)
            param = input("Choice? (1-4): ").strip()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt, Quitting...")


def main() -> None:
    """Parse command-line arguments and start the user interface."""

    if len(sys.argv) == 2:
        file = sys.argv[1]
        ui(file)
    else:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)


if __name__ == "__main__":
    main()

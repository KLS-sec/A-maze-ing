#!/usr/bin/env python3

"""Terminal interface and maze rendering utilities."""

from colorama import Fore, Style, init
import os
import sys
from pydantic import BaseModel, Field, model_validator, ValidationError
import re
from maze_generator import maze_generator
from maze_generator.maze_generator import MazeGenerator
from config_parsing import Config


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


def get_colors(index: int) -> dict:
    """Return the color scheme associated with the given index."""
    return COLOR_SCHEMES[index]


def rotate_colors(index: int) -> int:
    """Return the index of the next color scheme."""
    return (index + 1) % len(COLOR_SCHEMES)


def color_map(
    maze: list[list[maze_generator.Cell]],
    height: int,
    width: int,
    color_ind: int,
    show_path: bool,
) -> None:
    """Display the maze using the selected color scheme."""
    colors = get_colors(color_ind)

    def _colorize(key: str) -> str:
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
                maze,
                x,
                y,
                show_path,
            )

            for keys in lst_walls.keys():
                if keys == "upper_is_way_out" and show_path:
                    print(
                        colors["path"] + lst_walls[keys] + Style.RESET_ALL,
                        end="",
                    )
                else:
                    print(
                        _colorize(keys) + lst_walls[keys] + Style.RESET_ALL,
                        end="",
                    )

        print(colors["wall"] + "o" + Style.RESET_ALL)

        # Render left walls.
        for x in range(width):
            cell = maze[y][x]
            lst_walls = cell.get_left_wall(maze, x, y, show_path)

            for keys in lst_walls.keys():
                if (
                    keys == "left_is_way_out"
                    or keys == "center_is_way_out"
                ) and show_path:
                    print(
                        colors["path"] + lst_walls[keys] + Style.RESET_ALL,
                        end="",
                    )
                else:
                    print(
                        _colorize(keys) + lst_walls[keys] + Style.RESET_ALL,
                        end="",
                    )

        print(colors["wall"] + "o" + Style.RESET_ALL)

    print(colors["wall"] + "oooo" * width + "o" + Style.RESET_ALL)


class config_storage(BaseModel):
    """Validate configuration values loaded from the configuration file."""

    width: int = Field(ge=2, le=50)
    height: int = Field(ge=2, le=20)
    entry: list[int]
    exit: list[int]
    output_file: str
    perfect: bool

    @model_validator(mode="after")
    def checker(self) -> "config_storage":
        """Perform additional validation on configuration values."""

        if len(self.entry) != 2:
            raise ValueError("Entry error, invalid coordinates")

        if len(self.exit) != 2:
            raise ValueError("Exit error, invalid coordinates")

        if (
            self.entry[0] < 0
            or self.entry[0] >= self.width
            or self.entry[1] < 0
            or self.entry[1] >= self.height
        ):
            raise ValueError("Entry error, invalid coordinates")

        if (
            self.exit[0] < 0
            or self.exit[0] >= self.width
            or self.exit[1] < 0
            or self.exit[1] >= self.height
        ):
            raise ValueError("Exit error, invalid coordinates")

        if not re.fullmatch(r"[A-Za-z0-9_]+\.txt", self.output_file):
            raise ValueError(
                "OUTPUT_FILE must contain only letters, numbers, '_'"
                " and end with .txt"
            )

        return self


def get_config(filename: str) -> Config:
    """Load and validate configuration data from a file.

    Read configuration values from the specified file, convert them to
    their expected types, and validate them using the configuration
    model.

    Returns:
        Validated configuration data.

    Raises:
        SystemExit: If the file cannot be read or contains invalid
            configuration data.
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
                            raise ValueError(
                                "Entry or Exit error, invalid"
                                " coordinates.\nExemple: 5,8"
                            )

                        if parts[0].isdigit() and parts[1].isdigit():
                            if key == "ENTRY":
                                config.entry = [
                                    int(parts[0]),
                                    int(parts[1]),
                                ]
                            else:
                                config.exit = [
                                    int(parts[0]),
                                    int(parts[1]),
                                ]
                        else:
                            raise ValueError(
                                "Entry or Exit error, invalid"
                                " coordinates.\nExemple: 5,8"
                            )
                    else:
                        raise ValueError(
                            "Entry or Exit error, invalid "
                            "coordinates.\nExemple: 5,8"
                        )

                if key == "OUTPUT_FILE":
                    if not value.endswith(".txt"):
                        raise ValueError(
                            "OUTPUT_FILE error, invalid name"
                        )

                if key == "PERFECT":
                    if value == "True":
                        config.perfect = True
                    elif value == "False":
                        config.perfect = False
                    else:
                        raise ValueError(
                            "Type error, what kind of maze do you"
                            " want?"
                        )

                if key == "SEED":
                    if value == "True":
                        config.seed = True
                    elif value == "False":
                        config.seed = False

        try:
            tester = config_storage(
                width=config.width,
                height=config.height,
                entry=config.entry,
                exit=config.exit,
                output_file=config.output_file,
                perfect=config.perfect,
            )

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


def render(
    maze: list[list[maze_generator.Cell]],
    height: int,
    width: int,
    color_ind: int,
    show_path: bool,
) -> None:
    """Clear the terminal and display the maze."""

    if maze:
        os.system("cls" if os.name == "nt" else "clear")
        color_map(maze, height, width, color_ind, show_path)


def gen_maze(
    mazegen: MazeGenerator,
) -> list[list[maze_generator.Cell]]:
    """Generate and solve a maze."""

    map = mazegen.generate()
    maze = mazegen.solve(map)

    return maze


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

    maze_generator.generate_output_file(
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

                maze_generator.generate_output_file(
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

                maze_generator.generate_output_file(
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


def main():
    """Parse command-line arguments and start the user interface."""

    if len(sys.argv) == 2:
        file = sys.argv[1]
        ui(file)
    else:
        raise Exception(
            "Incorrect arguments, "
            "expected : python3 print_term 'config file'"
        )


if __name__ == "__main__":
    main()

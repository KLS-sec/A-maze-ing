from colorama import Fore, Style, init
import os
import sys
from maze_generator import maze_generator


init(autoreset=True)  # reset de couleurs


# combinaison de couleurs
COLOR_SCHEMES = [
    {"wall": Fore.WHITE, "start": Fore.BLUE, "exit": Fore.RED,
     "ft": Fore.MAGENTA, "path": Fore.GREEN},  # combinaison 1
    {"wall": Fore.CYAN,  "start": Fore.YELLOW, "exit": Fore.BLUE,
     "ft": Fore.GREEN, "path": Fore.RED},  # combinaison 2
    {"wall": Fore.BLUE,  "start": Fore.GREEN,  "exit": Fore.MAGENTA,
     "ft": Fore.RED,     "path": Fore.YELLOW},  # combinaison 3
]


# renvoie une combinaison de couleurs
def get_colors(index: int) -> dict:
    return COLOR_SCHEMES[index]


# rotation couleur cyclique avec COLOR_SCHEMES
def rotate_colors(index: int) -> int:
    return (index + 1) % len(COLOR_SCHEMES)


# colorie le maze
def color_map(maze: list[list[maze_generator.Cell]], height: int, width: int,
              color_ind: int, show_path: bool) -> None:
    colors = get_colors(color_ind)  # une combinaison de couleurs
    # colorie le mur (haut ou gauche)

    def _colorize(key: str) -> str:
        if (key == "upper_is_ft" or
            key == "upper_left_is_ft" or
            key == "left_is_ft" or
                key == "center_is_ft"):
            return colors["ft"]
        if key == "center_is_start":
            return colors["start"]
        if key == "center_is_exit":
            return colors["exit"]
        return colors["wall"]

    for y in range(height):
        # boucle sur les murs du haut
        for x in range(width):
            cell = maze[y][x]
            lst_walls: dict[str, str] = cell.get_upper_wall(maze, x,
                                                            y, show_path)
            for keys in lst_walls.keys():
                if keys == "upper_is_way_out" and show_path:
                    print(colors["path"] + lst_walls[keys] + Style.RESET_ALL,
                          end="")
                else:
                    print(_colorize(keys) + lst_walls[keys] + Style.RESET_ALL,
                          end="")
        print(colors["wall"] + "o" + Style.RESET_ALL)

        # boucle sur les murs de gauche
        for x in range(width):
            cell = maze[y][x]
            lst_walls = cell.get_left_wall(maze, x, y, show_path)
            for keys in lst_walls.keys():
                if (
                    keys == "left_is_way_out" or keys == "center_is_way_out"
                ) and show_path:
                    print(colors["path"] + lst_walls[keys] + Style.RESET_ALL,
                          end="")
                else:
                    print(_colorize(keys) + lst_walls[keys] + Style.RESET_ALL,
                          end="")
        print(colors["wall"] + "o" + Style.RESET_ALL)

    print(colors["wall"] + "oooo" * width + "o" + Style.RESET_ALL)


# execute color_map pour obtenir le maze coloré
def render(maze: list[list[maze_generator.Cell]], height: int, width: int,
           color_ind: int, show_path: bool) -> None:
    if maze:
        os.system("cls" if os.name == "nt" else "clear")  # ****
        color_map(maze, height, width, color_ind, show_path)


def gen_maze(data: maze_generator.Config) -> list[list[maze_generator.Cell]]:

    maze = maze_generator.maze_creator(data.height, data.width)
    maze_generator.fourtier(maze, data.height, data.width)
    maze_generator.atributor_start(maze, data.entry)
    maze_generator.atributor_exit(maze, data.exit)
    maze_generator.wanderer(maze, data.entry, data)
    if not data.perfect:
        maze_generator.imperfect_maker(maze, data)
        maze_generator.imperfect_solver(maze, data)
    return maze


# interface ancien
def ui(filename: str) -> None:
    show_path = True
    color_ind = 0
    data = maze_generator.get_config(filename)
    mazegen = gen_maze(data)
    maze_generator.generate_output_file(data.output_file, mazegen, data.entry,
                                        data.exit, data.path)
    render(mazegen, data.height, data.width, color_ind, show_path)
    txt = ("=== a-maze-ing ===\n"
           "1. Re-generate a new maze\n"
           "2. Show/Hide path from entry to exit\n"
           "3. Rotate maze colors\n"
           "4. Quit")
    print(txt)
    try:
        param = input("Choice? (1-4): ").strip()
        while param != "4":
            if param == "1":
                mazegen = gen_maze(data)
                maze_generator.generate_output_file(data.output_file, mazegen,
                                                    data.entry,
                                                    data.exit, data.path)
                render(mazegen, data.height, data.width, color_ind, show_path)
            elif param == "2":
                show_path = not show_path
                render(mazegen, data.height, data.width, color_ind, show_path)
            elif param == "3":
                color_ind = rotate_colors(color_ind)
                render(mazegen, data.height, data.width, color_ind, show_path)
            else:
                mazegen = gen_maze(data)
                maze_generator.generate_output_file(data.output_file, mazegen,
                                                    data.entry,
                                                    data.exit, data.path)
                render(mazegen, data.height, data.width, color_ind, show_path)
            print(txt)
            param = input("Choice? (1-4): ").strip()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt, Quitting...")


def main():
    if len(sys.argv) == 2:
        file = sys.argv[1]
        ui(file)
    else:
        raise Exception("Incorrect arguments, "
                        "expected : python3 print_term 'config file'")


if __name__ == "__main__":
    main()

from colorama import Fore, Style, init
import os
from maze_map import Cell


init(autoreset=True)  # reset de couleurs


# combinaison de couleurs
COLOR_SCHEMES = [
    {"wall": Fore.WHITE, "start": Fore.BLUE, "exit": Fore.RED,
     "ft": Fore.MAGENTA, "path": Fore.YELLOW},  # combinaison 1
    {"wall": Fore.CYAN,  "start": Fore.YELLOW, "exit": Fore.MAGENTA,
     "ft": Fore.GREEN, "path": Fore.RED},  # combinaison 2
    {"wall": Fore.BLUE,  "start": Fore.GREEN,  "exit": Fore.YELLOW,
     "ft": Fore.RED,     "path": Fore.MAGENTA},  # combinaison 3
]


# renvoie une combinaison de couleurs
def get_colors(index: int) -> dict:
    return COLOR_SCHEMES[index]


# rotation couleur cyclique avec COLOR_SCHEMES
def rotate_colors(index: int) -> int:
    return (index + 1) % len(COLOR_SCHEMES)


# colorie le maze
def color_map(maze: list[list[Cell]], height: int, width: int,
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
            lst_walls = cell.get_upper_wall(maze, x, y, show_path)
            for keys in lst_walls.keys():
                if keys == "upper_is_way_out" and show_path:
                    print(colors["path"] + lst_walls[keys] + Style.RESET_ALL, end="")
                else:
                    print(_colorize(keys) + lst_walls[keys] + Style.RESET_ALL, end="")
        print(colors["wall"] + "█" + Style.RESET_ALL)

        # boucle sur les murs de gauche
        for x in range(width):
            cell = maze[y][x]
            lst_walls = cell.get_left_wall(maze, x, y, show_path)
            for keys in lst_walls.keys():
                if (keys == "left_is_way_out" or keys == "center_is_way_out") and show_path:
                    print(colors["path"] + lst_walls[keys] + Style.RESET_ALL, end="")
                else:
                    print(_colorize(keys) + lst_walls[keys] + Style.RESET_ALL, end="")
        print(colors["wall"] + "█" + Style.RESET_ALL)

    print(colors["wall"] + "█" + "▇▇▇▇" * (width-1) + "▇▇▇█" + Style.RESET_ALL)


# execute color_map pour obtenir le maze coloré
def render(maze: list[list[Cell]], height: int, width: int,
           color_ind: int, show_path: bool) -> None:
    if maze:
        os.system("cls" if os.name == "nt" else "clear")
        color_map(maze, height, width, color_ind, show_path)


def gen_maze() -> list[list[Cell]]:
    from maze_map import maze_creator
    from role_atribution import atributor_start, atributor_exit, fourtier
    from way_maker import wanderer
    from get_config import get_config

    data = get_config("config.txt")
    height = data["HEIGHT"]
    width = data["WIDTH"]
    maze = maze_creator(height, width)
    fourtier(maze, height, width)
    atributor_start(maze, data["ENTRY"])
    atributor_exit(maze, data["EXIT"])
    wanderer(maze, data["ENTRY"], data)
    return maze


# interface ancien
def ui(height: int, width: int) -> None:
    show_path = True
    color_ind = 0
    mazegen = gen_maze()
    render(mazegen, height, width, color_ind, show_path)
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
                mazegen = gen_maze()
                render(mazegen, height, width, color_ind, show_path)
            elif param == "2":
                show_path = not show_path
                render(mazegen, height, width, color_ind, show_path)
            elif param == "3":
                color_ind = rotate_colors(color_ind)
                render(mazegen, height, width, color_ind, show_path)
            else:
                mazegen = gen_maze()
                render(mazegen, height, width, color_ind, show_path)
            print(txt)
            param = input("Choice? (1-4): ").strip()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt, Quitting...")


if __name__ == "__main__":
    from get_config import get_config

    data = get_config("config.txt")
    height = data["HEIGHT"]
    width = data["WIDTH"]
    ui(height, width)

from maze_generator.maze_generator import Cell, Wall, Maze_Generator
from random import choice
from parser import create_interpreter
from enum import Enum
import sys
import os


class Color(Enum):
    """WALL_FONT combination of colors"""
    RESET = "\033[0m"
    P_B = "\033[38;5;198m\033[48;5;250m"
    VC_R = "\033[38;5;196m\033[48;5;58m"
    B_J = "\033[38;5;27m\033[48;5;221m"
    BF_R = "\033[38;5;19m\033[48;5;212m"
    B_G = "\033[38;5;255m\033[48;5;236m"
    V_V = "\033[38;5;46m\033[48;5;183m"
    B_W = "\033[38;5;232m\033[48;5;255m"


def display_wall(maze: Maze_Generator, wall: Wall) -> str:

    walls = {'1111': '─┼─',  # ensw
             '1110': ' ├─',  # ens
             '0111': '─┴─',  # enw
             '1101': '─┬─',  # esw
             '1100': ' ┌─',  # es
             '0110': ' └─',  # en
             '0101': '───',  # ew
             '0100': ' ╶─',  # e
             '1011': '─┤ ',  # nsw
             '1010': ' │ ',  # ns
             '0011': '─┘ ',  # nw
             '1001': '─┐ ',  # sw
             '1000': ' ╷ ',  # s
             '0010': ' ╵ ',  # n
             '0001': '─╴ ',  # w
             '0000': '   '}

    if wall.path is False:
        if wall.maze_y+1 <= maze.height*2:
            if isinstance(maze.list_y_x[wall.maze_y+1][wall.maze_x], Wall):
                if maze.list_y_x[wall.maze_y+1][wall.maze_x].path is False:
                    wall.next[0] = '1'
                else:
                    wall.next[0] = '0'
            else:
                wall.next[0] = '0'
        else:
            wall.next[0] = '0'

        if wall.maze_y-1 >= 0:
            if isinstance(maze.list_y_x[wall.maze_y-1][wall.maze_x], Wall):
                if maze.list_y_x[wall.maze_y-1][wall.maze_x].path is False:
                    wall.next[2] = '1'
                else:
                    wall.next[2] = '0'
            else:
                wall.next[2] = '0'
        else:
            wall.next[2] = '0'

        if wall.maze_x+1 <= maze.width*2:
            if isinstance(maze.list_y_x[wall.maze_y][wall.maze_x+1], Wall):
                if maze.list_y_x[wall.maze_y][wall.maze_x+1].path is False:
                    wall.next[1] = '1'
                else:
                    wall.next[1] = '0'
            else:
                wall.next[1] = '0'
        else:
            wall.next[1] = '0'

        if wall.maze_x-1 >= 0:
            if isinstance(maze.list_y_x[wall.maze_y][wall.maze_x-1], Wall):
                if maze.list_y_x[wall.maze_y][wall.maze_x-1].path is False:
                    wall.next[3] = '1'
                else:
                    wall.next[3] = '0'
            else:
                wall.next[3] = '0'
        else:
            wall.next[3] = '0'

        return walls.get("".join(wall.next), '')

    else:
        return '   '


def reset_ansi_color() -> None:
    print(Color.RESET.value)


def set_ansi(maze: Maze_Generator) -> None:
    all_colors = [color for color in Color if color != Color.RESET]
    lab_choice = choice(all_colors)
    maze.lab_color = lab_choice.value

    all_bg_fortytwo = [f"\033[38;5;{x}m\033[48;5;{x}m" for x in range(10, 15)]
    maze.fortytwo_color = choice(all_bg_fortytwo)


'''def make_output(maze: Maze_Generator) -> str:
    layout: str = str()
    pos_x: int = 0

    for y in maze.list_y_x:
        for x in y:
            current_color = (maze.fortytwo_color
                             if x.isfortytwo else maze.lab_color)

            if isinstance(x, Cell | Wall):
                if isinstance(x, Cell) and x.is_entry:
                    layout += "\033[42me n\033[0m"
                elif isinstance(x, Cell) and x.is_exit:
                    layout += "\033[43me x\033[0m"
                elif x.a_way_out and maze.display_path:
                    layout += "\033[41m   \033[0m"
                else:
                    if isinstance(x, Cell):
                        layout += "   "

            if isinstance(x, Wall):
                if x.a_way_out is False or maze.display_path is False:
                    layout += (current_color +
                               display_wall(maze, x) +
                               maze.lab_color)

            pos_x += 1
            if pos_x == maze.width*2+1:
                layout += "\n"
                pos_x = 0
    return layout'''


def make_output(maze: Maze_Generator) -> str:
    layout: str = ""
    pos_x: int = 0

    for y in maze.list_y_x:
        for x in y:
            current_color = (maze.fortytwo_color
                             if x.isfortytwo else maze.lab_color)

            if isinstance(x, Cell):
                if x.is_entry:
                    layout += "\033[42me n\033[0m"
                elif x.is_exit:
                    layout += "\033[43me x\033[0m"
                elif x.a_way_out and maze.display_path:
                    layout += "\033[41m   \033[0m"
                else:
                    layout += current_color + "   " + Color.RESET.value

            elif isinstance(x, Wall):
                glyph = display_wall(maze, x)
                if x.a_way_out and maze.display_path:
                    layout += "\033[41m" + glyph + Color.RESET.value
                else:
                    layout += current_color + glyph + Color.RESET.value

            pos_x += 1
            if pos_x == maze.width*2+1:
                layout += "\n"
                pos_x = 0
    return layout


def main() -> None:
    try:
        maze_config = create_interpreter()
        if maze_config is None:
            return
        os.system('clear')
        if maze_config is not None:
            maze = Maze_Generator(maze_config.height, maze_config.width,
                                  maze_config.perfect)
            loop_number = '0'

            if maze.check_term_size():
                maze.init_maze()
                set_ansi(maze)
                if maze.height > 6 and maze.width > 8:
                    maze.make_fortytwo()
                maze.check_coordinates(maze_config.entry, maze_config.exit)
                maze.iterative_backtracking(maze_config.seed)
                maze.solve_bfs(maze_config.entry, maze_config.exit)
                print(f"{make_output(maze)}")
                if maze.height <= 6 or maze.width <= 8:
                    print("\nMaze too small to generate the 42 pattern\n")
                maze.save_maze_to_file(maze_config.output, maze_config.entry,
                                       maze_config.exit)

            while loop_number != '4' and maze.check_term_size():
                loop_number = input("Enter 1 to regenerate labyrinth\n"
                                    "Enter 2 to change labyrinth color\n"
                                    "Enter 3 to show or hide path\n"
                                    "Enter 4 to quit\n")

                if loop_number == '1':
                    maze.iterative_backtracking(maze_config.seed)
                    maze.solve_bfs(maze_config.entry, maze_config.exit)
                    os.system('clear')
                    print(f"{make_output(maze)}")
                    maze.save_maze_to_file(maze_config.output,
                                           maze_config.entry, maze_config.exit)

                elif loop_number == '2':
                    set_ansi(maze)
                    os.system('clear')
                    print(f"{make_output(maze)}")

                elif loop_number == '3':
                    if maze.display_path:
                        maze.display_path = False
                    else:
                        maze.display_path = True
                    os.system('clear')
                    print(f"{make_output(maze)}")

                elif loop_number == '4':
                    reset_ansi_color()
                    sys.exit()
    except Exception as e:
        a = str(e)
        print(a.capitalize(), "\nThe program will now close", sep="")
        reset_ansi_color()


if __name__ == "__main__":
    main()

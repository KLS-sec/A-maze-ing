*This project has been created as part of the 42 curriculum by lching, kbrun.*

# Description  
We implemented a **maze generator in Python** that takes a *configuration file*, generates a maze, usually perfect (with a single path connecting all parts of the maze), and writes it to a file using a hexadecimal wall representation. We also made a visual of the maze in ASCII representation and organized our code so that the generation logic can be reused later.  
By using a config.txt file as an argument given to the program, we will generate the labyrinth depending on the option given in the text file : its width, height, the entry and exit point, the name of the output file, if the labyrinth is perfect or not, the seed used to generate the same labyrinth and which algorithm we used to generate the labyrinth and the shortest path to the exit.
We also generate an output file named **maze.txt** which gives an hexadecimal representation of the labyrinth followed by the entry point, the exit point and the shortest valid path from entry to exit, written with a succession of **N(orth), S(outh), E(ast), W(est), as each hex digit represents the 4 walls of a cell in North-East-South-West order


# Instructions  
Use the command **"python3 a_maze_ing.py config.txt"** to launch the program if all dependancies from requirements.txt are already installed.

Another way to launch it without dependancies, is to use the command **"make install"** as it will create a virtual environment with all the conditions necessary to launch the program.

The second command to use would be **"make run"**, which should lead to the creation of the maze and the path from entry to exit if all parameters from *config.txt* had been correctly set up, as well as a *menu* from 1 to 4, where the user can choose one of which to change the output of the labyrinth :
- **1** : Change the *arrangement* of the labyrinth, usually leading to a new path from entry to exit too, without changing any base parameters.
- **2** : Change only the color of the font, the 42 pattern (if visible) and the walls of the labyrinth from a preset *ANSI CODES*.
- **3** : Show or Hide the path from *start* (in green) to *end point* (in yellow).
- **4** : *Reset* the terminal to its base color and *exit* the program.

There is also **"make debug"** to get to the debugger pdb and test the file as it is, line by line.

**"make clean / uninstall"** are used to remove cached datas or temporary files, while the 2nd command **"uninstalled"** remove also the virtual environment.

Finally, **"make lint / lint-strict"** are commands to type-check with *mypy* and see all *flake8* errors, the first one having a few flags to check our files while the 2nd is checking everything.
# Resources
A video to understand the basic concept of some possible choices of algorithm to [generate a maze](https://www.youtube.com/watch?v=ioUl1M77hww).

Another one to see how the breadth first search algorithm works to look for the [shortest path to solution](https://www.youtube.com/watch?v=V1oZQm1HtVw).

The [ANSI Color Codes](https://gist.github.com/JBlond/2fea43a3049b38287e5e9cefc87b2124) site to create all the colors within our labyrinth.

AI was used to correct a few mistakes we made on the way and to improve our understanding of how to not miss those kinds of mistakes anymore. 

# Additional Sections
## Config.txt
**config.txt** is a text file that *setup the maze outlines* with some basic parameters such as **height and width or entry and exit**. Those four parameters must be within the *range of 2 to 40 (30 for height)*, otherwise the program will choose a *default value* for **width and height** or exit completely for **entry or exit errors**, such as the same entry and exit point, one of them outside of the labyrinth range, if you write a negative or float... All others parameters has a *default value* too if you try to change or remove them for anything not within expectation.

If some changes needs to be done for the *config.txt file*, here is a basic example of how to handle the configurations of all parameters :
- WIDTH=*positive integer*
- HEIGHT=*positive integer*
- ENTRY=*positive integer*,*positive integer*
- EXIT=*positive integer*,*positive integer*
- OUTPUT_FILE=*maze.txt*
- PERFECT=*True or False*
- SEED=*positive integer*
- ALGORITHM=*"Backtracking"*

## Algorithms chosen
We used a variant of the **Recursive Backtracking** as it was implemented with **Iteration** instead of some callbacks of the algorithm, as it used far less memory and allow us to generate a bigger labyrinth faster than the recursive limit would have done by itself.  
It is a **DFS algorithm** *(Depth-First Search)* which was chosen for its ability to create **perfect mazes** (no loops, every cell is reachable) with long, winding corridors and fewer dead ends compared to other algorithms.  
The 2nd algorithm we implemented was a **BFS algorithm** *(Breadth First Search)*, which was chosen because it explores all possible paths of the present depth before searching for the next layer, mathematically guaranteeing the **shortest path** between the entry and exit points.

The *first algorithm* use the principle of a **stack** *(FILO, First In Last Out)*, where you add the first path and *explore it to its limit*, and if no way out was found, *trackback* every cell one by one, as if it was *lead by a thread*, until we find another *neighbouring cell unexplored*.  
The other algorithm on the other end, use the opposite principle by using a **queue** (FIFO, First In First Out) to explore all possible cell within its reach and dropping the ones that lead to a deadend.

## Reusability
### Installation
`pip install mazegen-1.0.0-py3-none-any.whl`

## Usage
```python
from maze_generator.maze_generator import Maze_Generator

# Instanciation with personalized parameters
maze = Maze_Generator(height=20, width=20)
maze.init_maze()
maze.iterative_backtracking(seed=142417)

# Accessing structure and solution (do your own output file)
maze.solve_bfs(entry=(0,0), exit=(1,1))
output = maze.make_output()
print(output)
```
## Management
### Planning
*   **Phase 1:** **Grid structure** design and **ASCII rendering logic** of the maze, creating basic files with their base structure needed for the project, such as the parser and a_maze_ing file, maze_generator folder, this README.MD, the Makefile...
*   **Phase 2:** Implementation of the **Recursive Backtracking algorithm** to create a true and *"perfect"* labyrinth by *"breaking" the walls* as the algorithm goes through, implementing the **color and the 42 pattern**.
*   **Phase 3:** **Pathfinding logic (BFS)** to create an *entry and exit point and the way in between* and the **hexadecimal export**, which gives a representation of the labyrinth wall, its entry and exit point.
*   **Phase 4:** **Packaging** with *build* (`mazegen-1.0.0-py3-none-any.whl`, `pyproject.toml`), **linting and correcting mistakes** from the *program*, the *config file* or *Makefile* and completing the *README.md* file.

### Improvement
The wall used at first was some **basic ASCII characters** such as "|", "_" or "-", but we quickly saw how limited our choice were with only those characters. After discovering *more options* such as "┼" or "┐", we implemented those to adapt to our labyrinth, which allowed a better **path management and walls structures.**

The possibility for the labyrinth to **react to the size of the terminal** and stop the program depending on if the labyrinth size would be too big compared to the terminal, which would create some artefacts and bugs on the display part.

The **choice of color**, as we thought first that only a handful of color was available to us, but we discovered the *ANSI color codes website* which allowed more diversity, and removed the possibility of mixing up colors of the same type between the walls, the 42 pattern, the path, its entry and exit point and the font. 

### Tools used
- **Python 3.10+**: It's the main language used to realize this labyrinth.
- **Mypy / Flake8**: Essential for static type checking and PEP8 compliance.
- **Setuptools / Build**: To create the `.whl` package as a module.

### Contributions
**lching** contributed to the project by creating the basic structure of the maze, making the Maze, Cell and Wall classes, finding the wall characters and allowing us to work on a way to display the maze. Also made the 42 pattern and helped improve the output of the maze and the colors of the full implementation.  
Created the function to convert the boolean representation of our walls to a binary number, which needed a transformation in hexadecimal representation for the maze.txt file. Helped a lot in correcting and improving bits by bits some part of the codes that needed to adapt to some new implementation or didn't worked as intended.

**kbrun** contributed to the project by doing the parser file and the BaseModel class to interpret the config.txt file wit hthe right conditions, made the Makefile and the basic structure of this README.  
Created the algorithms to dig in the closed walls and show the best path from entry to exit point and made a basic function and Enum class to color everything. Transformed the maze_generator folder as a reusable package to use for a later purpose. Also helped in correcting a few mistakes to fine-tune the labyrinth up to this shape.

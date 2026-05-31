*This project has been created as part of the 42 curriculum by mmakhmae, kle-scor*

## Description

The goal of the a-maze-ing project is to make a maze generator and solve it, that takes a configuration file, generates a maze, it can be perfect (single path between entrance and exit) or not. Also to make a output_file and writes it using hexadecimal representation of the maze to convert into cardinal point solution. This project also provides a visual representation of the maze in the terminal.

### Features:

- Custom configuration
- Default configuration file
- Seed system
- Generating algorithm
- Show 42 logo in the center of the maze
- Solving algorithm
- interface:
	- Regenerate maze
	- Hide/Show solving path
	- Rotate color
	- Quit
- Error handling
- Makefile
- Output file containing hexadecimal representation of the maze, the entrance and the exit and the solving path

### Output Format

In "output_file.txt":
```text
<hexadecimal representation of the maze>

<Entrance coordinates>
<Exit coordinates>
<Cardinal point string for the solving path>
```

### Config File Structure
```text
in "config.txt":
    - WIDTH=<int> > 1
    - HEIGHT=<int> > 1
    - ENTRY=<tuple> >= 0
    - EXIT=<tuple> >= 0
    - OUTPUT_FILE=<string>
    - PERFECT=True/False
optional parameter:
    - SEED=<int>
```

## Project Management
### Algorithm Choices & Justification

#### Perfect maze cration algorithm: depth-first search  
This algorythm will randomly move around the maze, tracing a single non linear line. When it is stuck it shrink from the end, or roolback, until the searching head find a new openable cell and start growing again.
Chosen for it's simplicity of use.

#### Perfect maze solving algorithm: None
Due to the way depth-first search work, at some point a perfect way is traced between start and exit. This program then send the solution to the "ariane_string" function that will modify the concerned cells and the maze creation continue.

#### Imperfect maze creation algorithm: conditionnal random wall break
First a perfect maze is made, then every cells with 3 wall will have one broken, allowing a maze with no dead end. Afterward a function will go in every cell one by ine and randomly chose to destriy a wall or not.
The density of walls can be chosen by changing the random range in
imperfect_maze.py -> imperfect_maker -> if random.randrange(0, 4) == 0:  
Chosen because it allow a control over the wall density and avoid any dead-end.

#### Imperfect maze solving algorithm: flood fill
Starting from the entry cell a line will grow, when a crossway is detected the line is copied and both will follow a different path. Every path will grow at the same time, like flooding the maze from the entry point. When one of the lines touche the exit it is detected as the shortest path and call the "ariane_string" function just like the perfect maze
Chosen for it's simplicity of use and the ability to solve any kind of maze. It present a weekness of being slow and ressource demanding on massive maze, but it could be optimized by eraising lines reaching a dead-end

## Reusable part
- ### MazeGenerator class

    This class handle the generation of the maze from a seed, including the 42 logo.
```python
    Attributes:
        config data (class Config): where Config includes :
			- width (int): The width of the maze. Must be greater or equal to 2
			- height (int): The hight of the maze. Must be greater or equal to 2
			- seed (int): The seed of the maze
			- entry (list[int]): A couple of coordinates that represent the entrance of the maze
			- exit (list[int]): A couple of coordinates that represent
				the entrance of the maze
			- output_file (str): the name of the generated output_file
			- perfect (bool): create multiple/one way(s) to finish the maze
			- path (list[list[int]]): the path to get to the end

	Methods:
		generate() -> list[list[Cell]]: generate a maze randomly
    	solve() -> list[list[Cell]]: solve maze
```

- ### Output generation system
```python
    Generate the hexadecimal view of the maze,
    the coordinates of the entrance and exit
    and the path from the entrance to the exit

    Arguments:
        filename (str): The path to the config file
        maze (MazeGenerator): The binary representation of the maze
        entry (tuple[int, int]): The coordinates of the entry
        exit (tuple[int, int]): The coordinates of the exit
```

### Task Allocation


- ### kle-scor :
	- Solving Algorithm
	- Generate Algorithm
	- Error Handling
	- Parsing
	- Debugging
	- Docstrings
	- README

- ### mmakhmae :
	- Output_file
	- Interface
	- Visual Maze
	- Debugging
	- Docstrings
	- Makefile
	- README


### Your anticipated planning and how it evolved until the end
kle-scor focus on the logic and internal work, mmakhmae focus on the display and all the orbital tasks.

It worked quite well, since the core ellements were fractionned and independent the connection of the dirrerent ellements together was easy and mmakhmae could focus on the various tasks without indherence from our different way of codding.

The problem was on the end, since we had a limited knowldge of each other code we had to take some time to explain it to each other.

### Have you used any specific tools? Which ones?
None, only the basic features of python.


# Instructions
### Installation
```bash
make install
```
### Debug
```bash
make debug
```
### Run
```bash
make run
```
### Lint
```bash
make lint
or
make lint-strict
```
### Remove cache files
```bash
make clean
```


## Resources

Documentation & Guides

Official 42 subject (a-maze-ing)

algorithm forums 

algorithm documentation


### AI Usage

AI was used in this project for:

Understanding and comparing different strategies.
Clarifying algorithm optimization techniques.
Find some bug.
Get informations about the specificity of some functions.

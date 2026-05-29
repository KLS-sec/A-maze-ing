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

... a remplir 


• What part of your code is reusable, and how.


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


◦ Your anticipated planning and how it evolved until the end

◦ What worked well and what could be improved

◦ Have you used any specific tools? Which ones?


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

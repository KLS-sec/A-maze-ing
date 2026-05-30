class Config:
    """Store all the data about the maze to be easily reused everywhere."""
    width: int = 0
    height: int = 0
    entry: list[int]
    exit: list[int]
    output_file: str = "output_maze.txt"
    perfect: bool = True
    seed: bool = False
    # store the shortest way from start to finish
    path: list[list[int]]

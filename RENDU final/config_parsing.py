class Config:
    width: int = 0
    height: int = 0
    entry: list[int]
    exit: list[int]
    output_file: str = "output_maze.txt"
    perfect: bool = True
    seed: bool = False
    path: list[list[int]]  # ****

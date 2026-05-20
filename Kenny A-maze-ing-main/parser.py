from typing import Any, Annotated, Optional
import sys
from pydantic import (BaseModel,
                      Field,
                      ValidationError,
                      model_validator)


class MazeInterpreter(BaseModel):
    width: Annotated[int, Field(ge=2, le=40)]
    height: Annotated[int, Field(ge=2, le=30)]
    entry: Annotated[tuple[int, int], Field(min_length=2, max_length=2)]
    exit: Annotated[tuple[int, int], Field(min_length=2, max_length=2)]
    output: Annotated[str, Field(min_length=5, max_length=50)]
    perfect: bool = True
    seed: Annotated[Optional[int], Field(default=None)]
    algorithm: Annotated[Optional[str],
                         Field(min_length=1, max_length=15)] = "Bactracking"

    @model_validator(mode="after")
    def validate_maze_rules(self) -> 'MazeInterpreter':

        if self.entry[0] >= self.height or self.entry[1] >= self.width:
            raise ValueError("Coordinates of entry is outside "
                             "range of labyrinth")

        if self.entry[0] < 0 or self.entry[1] < 0:
            raise ValueError("Coordinates of entry is outside "
                             "range of labyrinth")

        if self.exit[0] >= self.height or self.exit[1] >= self.width:
            raise ValueError("Coordinates of exit is outside "
                             "range of labyrinth")

        if self.exit[0] < 0 or self.exit[1] < 0:
            raise ValueError("Coordinates of exit is outside "
                             "range of labyrinth")

        if self.entry == self.exit:
            raise ValueError("Entry and exit must be different")

        if self.output != 'maze.txt':
            raise ValueError("You must write a maze.txt file for the output")

        if (not isinstance(self.algorithm, str)
           or (isinstance(self.algorithm, str)
           and self.algorithm.capitalize() != "Backtracking")):
            raise ValueError("Algorithm not recognized."
                             "Switching to 'Backtracking' algorithm")

        if self.algorithm == '':
            raise ValueError("Algorithm not recognized."
                             "Switching to 'Backtracking' algorithm")

        return self


def stock_config() -> dict[str, str]:
    """Parse and stock config.txt in a returned dictionnary"""
    config: dict[str, str] = dict()
    argv = sys.argv
    try:
        with open(argv[1], "r") as file:
            for line in file:
                key, value = line.strip().split("=")
                config.update({key.strip(): value.strip()})
    except (FileNotFoundError, PermissionError, IndexError) as e:
        print(str(e).capitalize(), "\nThe program will now close", sep="")
        sys.exit()
    return config


def typing_conf(config: dict[str, str]) -> dict[str, Any]:
    """Adapt and return parsed data to apply it to the code"""
    parsed: dict[str, Any] = dict()

    for key, value in config.items():
        if key == "ENTRY" or key == "EXIT":
            int_tuple = (int(value.split(",")[0]), int(value.split(",")[1]))
            parsed.update({key: int_tuple})
        if value.isdigit():
            value_int = int(value)
            parsed.update({key: value_int})
        if key == 'PERFECT' and (value == 'True' or value == 'False'):
            if value == 'True':
                value_bool = True
            else:
                value_bool = False
            parsed.update({key: value_bool})
        if key == "SEED":
            if isinstance(value, int):
                parsed.update({key: value})
        if key == "ALGORITHM" or key == "OUTPUT_FILE":
            parsed.update({key: value})
    return parsed


def create_interpreter() -> MazeInterpreter | None:
    config = stock_config()
    typed_data = typing_conf(config)

    try:
        interpreter = MazeInterpreter(
            width=typed_data.get("WIDTH", 11),
            height=typed_data.get("HEIGHT", 11),
            entry=typed_data["ENTRY"],
            exit=typed_data["EXIT"],
            output=typed_data.get("OUTPUT_FILE", "maze.txt"),
            perfect=typed_data.get("PERFECT", True),
            seed=typed_data.get("SEED", None),
            algorithm=typed_data.get("ALGO", "Backtracking")
        )
        print(interpreter)
        return interpreter
    except ValidationError as e:
        print(str(e.errors()[0]["loc"][0]).capitalize(),
              str.strip(e.errors()[0]["msg"], "Value error, "),
              "\nThe program will now close")
    return None

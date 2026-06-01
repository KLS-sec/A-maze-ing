from pydantic import BaseModel, Field, model_validator, ValidationError
import re
import sys
import random


class Config:
    """Store all the data about the maze to be easily reused everywhere."""
    width: int = 0
    height: int = 0
    entry: list[int]
    exit: list[int]
    output_file: str = "output_maze.txt"
    perfect: bool = True
    seed: str = "False"
    path: list[list[int]]


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
                    else:
                        Config.output_file = value

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
                    if value == "False":
                        config.seed = "False"
                    else:
                        random.seed(value)

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

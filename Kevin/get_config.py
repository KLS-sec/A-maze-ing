#!/usr/bin/env python3

# checked multiple times, should be good
from pydantic import BaseModel, Field, model_validator, ValidationError
import re
import sys


class config_storage(BaseModel):
    """Multiple check for the config file input."""
    width: int = Field(ge=2, le=50)
    height: int = Field(ge=2, le=18)
    entry: list[int]
    exit: list[int]
    output_file: str
    perfect: bool

    @model_validator(mode='after')
    def checker(self) -> "config_storage":
        if len(self.entry) != 2:
            raise ValueError("Entry error, invalid coordinates")
        if len(self.exit) != 2:
            raise ValueError("Exit error, invalid coordinates")
        if (
           self.entry[0] < 0 or self.entry[0] >= self.width or
           self.entry[1] < 0 or self.entry[1] >= self.height):
            raise ValueError("Entry error, invalid coordinates")
        if (
           self.exit[0] < 0 or self.exit[0] >= self.width or
           self.exit[1] < 0 or self.exit[1] >= self.height):
            raise ValueError("Exit error, invalid coordinates")

        if not re.fullmatch(r"[A-Za-z0-9_]+\.txt", self.output_file):
            raise ValueError(
                "OUTPUT_FILE must contain only letters, numbers, '_'"
                " and end with .txt"
            )
        return self


def get_config(filename: str) -> dict[str, bool | str | int | list]:
    """Retrieve the data from the indicated file.

    Retrieve every data, try to convert them into the correct type and
    send them in config_storage for further checking.

    Handle errors internally, raise them then terminate the program.

    Return dict with all the data ready to use

    Use:
        config = get_config("filename.txt")
    """
    config = {}
    try:
        with open("config.txt", "r") as a:
            for line in a:
                line = line.strip()
                if not line:
                    continue
                key, value = line.split("=")
                config[key] = value

                if key in {"WIDTH", "HEIGHT"}:
                    if value.isdigit():
                        config[key] = int(value)
                    else:
                        raise ValueError("Size error, invalid input")

                if key in {"ENTRY", "EXIT"}:
                    if "," in value:
                        parts = value.split(",")
                        if len(parts) != 2:
                            raise ValueError("Entry or Exit error, invalid"
                                             " coordinates.\nExemple: 5,8")
                        if parts[0].isdigit() and parts[1].isdigit():
                            config[key] = [int(parts[0]), int(parts[1])]
                        else:
                            raise ValueError("Entry or Exit error, invalid"
                                             " coordinates.\nExemple: 5,8")
                    else:
                        raise ValueError("Entry or Exit error, invalid "
                                         "coordinates.\nExemple: 5,8")

                if key == "OUTPUT_FILE":
                    if not value.endswith(".txt"):
                        raise ValueError("OUTPUT_FILE error, invalid name")

                if key == "PERFECT":
                    if value == "True":
                        config[key] = bool(True)
                    elif value == "False":
                        config[key] = bool(False)
                    else:
                        raise ValueError("Type error, what kind of maze do you"
                                         " want?")

                if key == "SEED":
                    if value == "True":
                        config[key] = bool(True)
                    elif value == "False":
                        config[key] = bool(False)

        try:
            tester = config_storage(width=config["WIDTH"],
                                    height=config["HEIGHT"],
                                    entry=config["ENTRY"],
                                    exit=config["EXIT"],
                                    output_file=config["OUTPUT_FILE"],
                                    perfect=config["PERFECT"])
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


# **** main de test, ne pas garder a la fin
def main() -> None:
    print("")
    a = get_config("config.txt")
    print(a)
    width = a["WIDTH"]
    height = a["HEIGHT"]
    entry = a["ENTRY"]
    exit = a["EXIT"]
    output_file = a["OUTPUT_FILE"]
    perfect = a["PERFECT"]
    seed = a["SEED"]
    print("")
    print(width, height, entry, exit, output_file, perfect, seed)


if __name__ == "__main__":
    main()

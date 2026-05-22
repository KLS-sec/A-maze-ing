#!/usr/bin/env python3

#  call ce programme dans un try except pour attraper les erreurs

from pydantic import BaseModel, Field, model_validator
import re

# **** ValidationError needed when calling this function in try - except


class config_storage(BaseModel):
    width: int = Field(ge=2, le=50)
    height: int = Field(ge=2, le=18)
    entry: list[int]  # **** check later that it does not overlap 42 symbol
    exit: list[int]  # **** check later that it does not overlap 42 symbol
    output_file: str
    perfect: bool
    seed: int | None  # **** what does it looks like?

    @model_validator(mode='after')
    def checker(self) -> "config_storage":
        if len(self.entry) != 2:
            raise ValueError("Entry error, invalid coordinates")
        if len(self.exit) != 2:
            raise ValueError("Exit error, invalid coordinates")
        if (
           self.entry[0] < 0 or self.entry[0] > self.width or
           self.entry[1] < 0 or self.entry[1] > self.height):
            raise ValueError("Entry error, invalid coordinates")
        if (
           self.exit[0] < 0 or self.exit[0] > self.width or
           self.exit[1] < 0 or self.exit[1] > self.height):
            raise ValueError("Exit error, invalid coordinates")

        if not re.fullmatch(r"[A-Za-z0-9_]+\.txt", self.OUTPUT_FILE):
            raise ValueError(
                "OUTPUT_FILE must contain only letters, numbers, '_'"
                " and end with .txt"
            )

        if self.seed < 1:  # ****check if strict > 0 or not
            raise ValueError("SEED error, invalid seed, must be a"
                             " positive int")


# quand il est call tout mettre dans un try/except pour saisir les erreurs
# get all the data
# **** lui faire tout mettre dans config storrage pour tester AVANT de return le dictionnaire
# j ai carrement oublie d utiliser la classe
def get_config(filename: str) -> dict[str, bool | str | int | list]:
    config = {}
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

            if key in {"ENTRY", "EXIT"}:  # secure formating, number, type
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
                # must be dealed with by pydantic (can detect "_")
                # maybe automatically add .txt
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
    return config


def main() -> None:
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

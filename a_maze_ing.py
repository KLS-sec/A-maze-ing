#  tout mettre dans un try/except pour saisir les erreurs
def get_config(filename: str) -> dict[str, bool | str | int | list]:
    config = {}
    with open("config.txt", "r") as a:
        for line in a:
            line = line.strip()
            if not line:
                continue
            key, value = line.split("=")
            config[key] = value
            print("Test")
            # secure input types ****
            # SEED is treated outside
            # value can remplace config[key] in some places
            if key in {"WIDTH", "HEIGHT"}:
                if value.isdigit():
                    config[key] = int(value)
                else:
                    exit()  # Error message and exit()/raise ****

            if key in {"ENTRY", "EXIT"}:  # secure formating, number, type
                if "," in value:
                    parts = value.split(",")
                    if len(parts) != 2:
                        exit()  # Error message and exit()/raise ****
                    if parts[0].isdigit() and parts[1].isdigit():
                        config[key] = [int(parts[0]), int(parts[1])]
                    else:
                        exit()  # Error message and exit()/raise ****
                else:
                    exit()  # Error message and exit()/raise ****

            if key == "OUTPUT_FILE":
                # must be dealed with by pydantic (can detect "_")
                # maybe automatically add .txt
                if not value.endswith(".txt"):
                    exit()  # Error message and exit()/raise ****

            if key == "PERFECT":
                if value == "True":
                    config[key] = bool(True)
                elif value == "False":
                    config[key] = bool(False)
                else:
                    exit()  # Error message and exit()/raise ****
    return config


def main() -> None:
    a = get_config("config.txt")
    print(a)
    b = ["o", "o", "o", "o", "o", "\n", "0", " ", " ", " ", "0", "\n", "o", "o", "o", "o", "o"]
    for x in b:
        print(x, end="")
    print("")

if __name__ == "__main__":
    main()


"""
def parse_value(key, value):
    value = value.strip()

    # tuple values like ENTRY=0,0
    if key in {"ENTRY", "EXIT()"}:
        return tuple(map(int, value.split(",")))

    # booleans
    if value.lower() == "true":
        return True

    if value.lower() == "false":
        return False

    # integers
    if value.isdigit():
        return int(value)

    # strings
    return value


def load_config(filename):
    config = {}

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()

            # skip empty lines
            if not line:
                continue

            key, value = line.split("=", 1)
            config[key] = parse_value(key, value)

    return config


config = load_config("data.txt")

print(config)

# usage examples
width = config["WIDTH"]
height = config["HEIGHT"]
entry = config["ENTRY"]
exit()_pos = config["EXIT()"]
output_file = config["OUTPUT_FILE"]
perfect = config["PERFECT"]
seed = config["SEED"]

print(width)
print(entry)
print(perfect)
"""

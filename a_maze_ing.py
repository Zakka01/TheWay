import sys
from maze.maze_solver import MazeSolver
from maze.maze_generator import MazeGenerator


def parse_config() -> dict:
    """
    Parse the Config File, Validate and Store the Data
    in a Dict, Handle the Error using try/Except to prevent
    Crashes
    """

    # Get Line, Strip it, Split based on '=', Store key value
    try:
        config = {}
        if len(sys.argv) > 1:
            filename = sys.argv[1]
            with open(filename, "r") as file:
                for line in file:
                    line = line.strip()
                    if line == "":
                        continue

                    elif line.startswith("#"):
                        continue

                    elif "=" not in line:
                        raise ValueError("Invalid Config Line")

                    else:
                        key, value = line.split("=", 1)
                        key, value = key.strip(), value.strip()
                        if key in config:
                            raise ValueError("Duplicate Lines")
                        config[key] = value
        else:
            raise IndexError("No Config File Given")

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    # Convert the Dict values into valide Data ready to Use
    try:
        for key, value in config.items():

            if key in ["ENTRY", "EXIT"]:
                x, y = value.split(",")
                x, y = int(x), int(y)
                if x < 0 or y < 0:
                    raise ValueError(f"{key} coordinates out of bounds")
                config[key] = (x, y)

            elif key in ["WIDTH", "HEIGHT", "SEED"]:
                try:
                    config[key] = int(value)
                except (TypeError, ValueError):
                    raise ValueError(f"'{value}' must be an int")

            elif key == "PERFECT":
                value = value.lower().capitalize()
                if (
                    value == "0"
                    or value == "1"
                    or value == "+1"
                    or value == "+0"
                    or value == "-0"
                ):
                    config[key] = int(value)
                elif value in ["True", "False"]:
                    config[key] = value == "True"
                else:
                    raise ValueError(
                        "'PERFECT' value must be (True - False - 0 or 1)"
                    )
            elif key == "ALGO":
                value = value.lower()
                if value not in ["dfs", "hak"]:
                    raise ValueError(f"{key} must be dfs or hak")
                config[key] = value

            elif key == "OUTPUT_FILE":
                lower_value = value.lower()
                if "." in value:
                    basename, format = lower_value.split(".", 1)
                    if format != "txt" or value == "":
                        raise ValueError(f"OUTPUT_FILE '{value}' is not valid")
                    config[key] = lower_value
                else:
                    raise ValueError("Output file format is Invalid")

    except Exception as err:
        print(f"ERROR: {err}", file=sys.stderr)
        sys.exit(1)

    return config


def init_program() -> None:
    print("\n=== A_Maze_ing ===")
    print("1. Re-generate a new maze")
    print("2. Show/Hide path from entry to exit")
    print("3. Rotate maze colors")
    print("4. Quit")


def start_program(maze: MazeGenerator) -> None:
    choice = int(input("Choice? (1-4): "))
    if choice == 1:
        pass
    elif choice == 2:
        pass
    elif choice == 3:
        pass
    elif choice == 4:
        exit()
    else:
        print(f"'{choice}' is not a valid choice!")
        start_program(maze)


def main() -> None:
    config = parse_config()  # Get config file result

    maze = MazeGenerator(config)
    solve = MazeSolver(maze)
    maze.grid_builder()

    # Get the Entry Coordinates from the config
    entry = config["ENTRY"]
    end = config["EXIT"]
    x, y = entry
    exit_x, exit_y = end

    start_block = maze.grid[y][x]
    end_block = maze.grid[exit_y][exit_x]

    maze.entry = start_block
    maze.exit = end_block

    maze.ft_pattern()
    if config["ALGO"] == "dfs":
        maze.dfs_generation(start_block)
    elif config["ALGO"] == "hak":
        maze.hunt_kill_generation()
    if not config["PERFECT"]:
        maze.random_loops()

    solve.solve_maze(start_block, end_block)

    # maze visualization
    maze.visual()

    try:
        hex_output = maze.hex_encoding()
        path = maze.path_direction()

        output_file = config["OUTPUT_FILE"]
        with open(output_file, "w") as f:
            for row in hex_output:
                f.write("".join(row) + "\n")

            f.write("\n")
            f.write(f"{x},{y}")
            f.write("\n")
            f.write(f"{exit_x},{exit_y}")

            f.write("\n")
            for p in path:
                f.write(p)
    except Exception as err:
        print(f"ERROR: {err}")

    init_program()
    start_program(maze)


if __name__ == "__main__":
    main()

import sys
import os
from maze.maze_generator import MazeGenerator, MazeSolver


def parse_config() -> dict:
    """
    Parse the Config File, Validate and Store the Data
    in a Dict, Handle the Error using try/Except to prevent
    Crashes
    """

    # Get Line, Strip it, Split based on '=', Store key value
    try:
        config: dict = {}
        valid_keys = [
            "WIDTH",
            "HEIGHT",
            "ENTRY",
            "EXIT",
            "OUTPUT_FILE",
            "PERFECT"]

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
                        key, value = key.strip().upper(), value.strip()
                        if not value:
                            raise ValueError(f"No Value Given '{key}'")
                        if key in config:
                            raise ValueError("Duplicate Lines")
                        if key not in valid_keys and not "SEED":
                            raise ValueError(f"Key: '{key}' is not Valid")

                        config[key] = value
        else:
            raise IndexError("No Config File Given")

        missing_keys = set(valid_keys) - set(config.keys())
        if missing_keys:
            raise ValueError(f"Missing keys: {missing_keys}")

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(0)

    # Convert the Dict values into valide Data ready to Use
    try:
        for key, value in config.items():

            if key in ["ENTRY", "EXIT"]:
                x_str, y_str = value.split(",")
                x = int(x_str)
                y = int(y_str)
                if x < 0 or y < 0:
                    raise ValueError(f"{key} coordinates out of bounds")
                config[key] = (x, y)

            elif key in ["WIDTH", "HEIGHT"]:
                try:
                    val = int(value)
                    if val <= 0:
                        raise ValueError()
                    config[key] = val
                except (TypeError, ValueError):
                    raise ValueError(f"{key}: '{val}' must be Positive"
                                     " number")

            elif key == "SEED":
                value = str(value).strip()
                try:
                    config[key] = int(value)
                except ValueError:
                    try:
                        config[key] = float(value)
                    except ValueError:
                        config[key] = value
                print(type(config[key]))

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

            elif key == "OUTPUT_FILE":
                # value = value.strip()
                lower_value = value.lower()

                if value == "":
                    raise ValueError(f"OUTPUT_FILE '{value}' is not valid")

                if " " in value or "/" in value:
                    raise ValueError(f"OUTPUT_FILE '{value}' is not valid")

                if "." not in value:
                    raise ValueError("Output file format is Invalid")

                basename, format = lower_value.rsplit(".", 1)

                if format != "txt" or basename == "":
                    raise ValueError(f"OUTPUT_FILE '{value}' is not valid")

                config[key] = lower_value

    except Exception as err:
        print(f"ERROR: {err}", file=sys.stderr)
        sys.exit(0)

    return config


def init_program(algo: str, maze: MazeGenerator) -> None:
    if algo == "hak":
        algo = "Hunt & Kill"
    if algo == "dfs":
        algo = "Depth first search - dfs"

    if maze.height <= 6 or maze.width <= 7:
        print(">> Maze too small, Can't display Pattern")
    print("\n=== A_Maze_ing ===")
    print("1. Re-generate a new maze")
    print("2. Show/Hide path from entry to exit")
    print("3. Rotate maze colors")
    print(f"4. Toggle Algorithm ({algo.upper()})")
    print("5. Quit")


def start_program(maze: MazeGenerator) -> int:
    try:
        user_input = int(input("Choice? (1-5): "))
        if 1 <= user_input <= 5:
            return user_input
        else:
            print(f"'{user_input}' is not a valid choice!")
            return start_program(maze)
    except (ValueError):
        print("Please enter a valid number.")
        return start_program(maze)


def main() -> None:
    try:
        config = parse_config()

        algo = "dfs"
        index = 0

        while True:
            try:
                maze = MazeGenerator(config)
                solve = MazeSolver(maze)
            except Exception as e:
                print(f"ERROR : {e}")
                exit(0)

            try:
                maze.grid_builder()
                if not maze.grid:
                    raise ValueError("Empty grid")

                # Get the Entry Coordinates from the config
                entry = config["ENTRY"]
                end = config["EXIT"]
                x, y = entry
                exit_x, exit_y = end
                if entry == end:
                    raise ValueError("entry and exit can't be in the "
                                     "same block")

                start_block = maze.grid[y][x]
                end_block = maze.grid[exit_y][exit_x]

                maze.entry = start_block
                maze.exit = end_block

                maze.ft_pattern()
            except Exception as e:
                print(f"Unexpected Error: {e}")
                exit(0)

            if algo == "dfs":
                maze.dfs_generation(start_block)
            elif algo == "hak":
                maze.hunt_kill_generation()

            if not config["PERFECT"]:
                maze.random_loops()

            solve.solve_maze(start_block, end_block)

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

            # User Interactions
            flag = 0
            while True:
                print(flush=True)
                os.system("clear")
                maze.visual(index)
                init_program(algo, maze)
                choice = start_program(maze)

                if choice == 1:
                    if maze.seed is None:
                        flag += 1
                        maze.seed = flag
                    break

                elif choice == 2:
                    maze.show_path = not maze.show_path

                elif choice == 3:
                    index = (index + 1) % 3

                elif choice == 4:
                    algo = "hak" if algo == "dfs" else "dfs"
                    break

                elif choice == 5:
                    print(">> Exiting...")
                    return
    except KeyboardInterrupt:
        print("\nProgram Interrupted")


if __name__ == "__main__":
    main()

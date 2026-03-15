import sys
import random

from maze.maze_solver import MazeSolver
from maze.maze_generator import MazeGenerator
from maze.maze_renderer import MazeRenderer


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

                    elif not "=" in line:
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
        print(f"ERROR: {e}", sys.stderr)
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

            elif key in ["WIDTH", "HEIGHT", "SEED", "PATTERN"]:
                config[key] = int(value)
            
            elif key == "PERFECT":
                value = value.lower().capitalize()
                if value not in ["True", "False"]:
                    raise ValueError(f"Invalid PERFECT value: {value}")
                config[key] = value == "True"

            elif key == "OUTPUT_FILE":
                if ".txt" not in value or value == "":
                    raise ValueError("OUTPUT_FILE is not valid")
                config[key] = value
    except Exception as err:
        print(f"ERROR: {err}", sys.stderr)
        sys.exit(1)

    return config



def main() -> None:

    config = parse_config()


    maze = MazeGenerator(config)
    maze.grid_builder()


    try:
        entry_x, entry_y = maze.entry
        exit_x, exit_y   = maze.exit

        # Make sure they are inside the maze
        if not (0 <= entry_x < maze.width and 0 <= entry_y < maze.height):
            raise ValueError(f"Entry coordinates {maze.entry} out of bounds")
        if not (0 <= exit_x < maze.width and 0 <= exit_y < maze.height):
            raise ValueError(f"Exit coordinates {maze.exit} out of bounds")

        start_block = maze.grid[entry_y][entry_x]
        end_block   = maze.grid[exit_y][exit_x]

    except ValueError as e:
        print(f"ERROR: {e}")
        exit(1)


    # generate and solve maze
    maze.start_generation(start_block)
    maze.generate_all()

    solve = MazeSolver(maze)
    solve.start_solving(start_block, end_block)



    if entry_y == 0:
        start_block.pop_wall("top")
    elif entry_y == maze.height - 1:
        start_block.pop_wall("bottom")
    elif entry_x == 0:
        start_block.pop_wall("left")
    elif entry_x == maze.width - 1:
        start_block.pop_wall("right")

    if exit_y == 0:
        end_block.pop_wall("top")
    elif exit_y == maze.height - 1:
        end_block.pop_wall("bottom")
    elif exit_x == 0:
        end_block.pop_wall("left")
    elif exit_x == maze.width - 1:
        end_block.pop_wall("right")


    try:
        hex_output = maze.hex_encoding()
        path = maze.path_direction()

        output_file = config["OUTPUT_FILE"]
        with open(output_file, "w") as f:
            for row in hex_output:
                f.write(''.join(row) + "\n")

            f.write("\n")
            f.write(f"{entry_x},{entry_y}")
            f.write("\n")
            f.write(f"{exit_x},{exit_y}")

            f.write("\n")
            for p in path:
                f.write(p)
    except Exception as err:
        print(f"ERROR: {err}")


    render = MazeRenderer(maze, solve)
    render.rendering()









if __name__ == "__main__":
    main()

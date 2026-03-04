import sys
from maze.maze_generator import Block, MazeGen


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

            elif key in ["WIDTH", "HEIGHT"]:
                config[key] = int(value)
            
            elif key == "PERFECT":
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
    maze = MazeGen(config)
    
    maze.grid_builder()
    



























if __name__ == "__main__":
    main()
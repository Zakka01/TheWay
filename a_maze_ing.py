# from maze.maze_generator import blabla
import sys

def Parse_config() -> dict:

    # parse file and store it in the dict
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
            raise Exception("No Config File Given")
    except Exception as e:
        print(f"ERROR CAUGHT: {e}")
        sys.exit(1)
        
    # convert to valid values
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
        print(f"ERROR: {err}")
        sys.exit(1)
        
    return dict   



if __name__ == "__main__":
    main()
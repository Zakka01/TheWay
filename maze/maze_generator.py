import random
from collections import deque


class Block:

    def __init__(self, y: int, x: int):
        """
            Initialize the attributes :
            x, y => ofc the coordinates,
            walls => if the block closed or not
            checked => if the block already visited or not
            ...
        """
        self.x = x
        self.y = y
        self.walls = {"top": True, "bottom": True, "left": True, "right": True}
        self.checked = False
        self.is_pattern = False
        self.is_path = False

    def has_wall(self, direction: str) -> bool:
        """
        check if block has wall in the given direction
        and return True if yes , otherwise False
        """
        if self.walls[direction] is True:
            return True
        return False

    def pop_wall(self, direction: str) -> None:
        """
        Mark the Direction as 'False' to Create Edge
        and Make the Two Blocks Connected
        """
        self.walls[direction] = False


class MazeGenerator:

    def __init__(self, config: dict):
        """
        Take the config dict as an Attribute
        while creating maze instance ,
        extract height and width
        """

        self.height = config["HEIGHT"]
        if self.height < 0:
            raise ValueError("Maze generation error")

        self.width = config["WIDTH"]
        if self.width < 0:
            raise ValueError("Maze generation error")

        self.entry = config["ENTRY"]
        x, y = self.entry
        if self.width < x < 0 or self.height < y < 0:
            raise ValueError("Maze generation error")

        self.exit = config["EXIT"]
        x, y = self.exit
        if self.width < x < 0 or self.height < y < 0:
            raise ValueError("Maze generation error")

        if "SEED" in config.keys():
            self.seed = config["SEED"]
        else:
            self.seed = None

        if "PERFECT" not in config.keys():
            config["PERFECT"] = True
        else:
            value = config.get("PERFECT")
            if value is not True and value is not False:
                raise ValueError("Maze generation error")

        if "OUTPUT_FILE" not in config.keys():
            config["OUTPUT_FILE"] = "maze.txt"
        else:
            value = str(config.get("OUTPUT_FILE")).strip()

            if not value.endswith(".txt"):
                raise ValueError("Maze generation error")

        self.grid: list = []
        self.solution: list = []
        self.show_path = False

    def grid_builder(self) -> None:
        """
        Build the Grid System Based On
        the HEIGHT &&& WIDTH from Config File
        """
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(Block(y, x))
            self.grid.append(row)

    def remove_wall_between(self, a: Block, b: Block) -> None:

        cx, cy = a.x, a.y
        nx, ny = b.x, b.y

        if cx < nx:
            a.pop_wall("right")
            b.pop_wall("left")

        elif cx > nx:
            a.pop_wall("left")
            b.pop_wall("right")

        elif cy > ny:
            a.pop_wall("top")
            b.pop_wall("bottom")

        elif cy < ny:
            a.pop_wall("bottom")
            b.pop_wall("top")

    def ft_pattern(self) -> None:
        """
        Get the Pattern value from config file
        - split the number and put them on list then
        loop thow each one and apply it to the maze
        as offset from the digit's center
        """

        cx = self.width // 2
        cy = self.height // 2

        four = [
            (cy - 2, cx - 3),
            (cy - 1, cx - 3),
            (cy, cx - 1),
            (cy, cx - 2),
            (cy, cx - 3),
            (cy, cx - 1),
            (cy + 1, cx - 1),
            (cy + 2, cx - 1),
        ]

        two = [
            (cy + 2, cx + 1),
            (cy + 2, cx + 2),
            (cy - 1, cx + 3),
            (cy + 2, cx + 3),
            (cy, cx + 1),
            (cy, cx + 2),
            (cy, cx + 3),
            (cy + 1, cx + 1),
            (cy - 2, cx + 1),
            (cy - 2, cx + 2),
            (cy - 2, cx + 3),
        ]

        for dy, dx in four:
            if 0 <= dy < self.height > 6 and 0 <= dx < self.width > 7:
                if (self.entry.x == dx) and (self.entry.y == dy):
                    raise ValueError("Entry coordinates are part "
                                     "or the 42 pattern")
                elif (self.exit.x == dx) and (self.exit.y == dy):
                    raise ValueError("Exit coordinates are part or"
                                     " the 42 pattern")
                self.grid[dy][dx].is_pattern = True

        for dy, dx in two:
            if 0 <= dy < self.height > 6 and 0 <= dx < self.width > 7:
                if (self.entry.x == dx) and (self.entry.y == dy):
                    raise ValueError("Entry coordinates are"
                                     "part or the 42 pattern")
                elif (self.exit.x == dx) and (self.exit.y == dy):
                    raise ValueError("Exit coordinates are part"
                                     " or the 42 pattern")
                self.grid[dy][dx].is_pattern = True

    def get_unvisited_neighbors(self, block: Block) -> list:
        """
        check the 4 possible neighbors while x & y
        are the coordinates, then we check the bounderies
        if valid, to append the valid neighbor to the list
        """
        valid_neighbors = []
        x, y = block.x, block.y

        neighbors = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]

        # loop over Neighbors & Add valid ones that hasn't checked yet
        for n in neighbors:
            nx, ny = n
            if 0 <= nx < self.width and 0 <= ny < self.height:
                this_block = self.grid[ny][nx]

                if not this_block.checked and not this_block.is_pattern:
                    valid_neighbors.append(this_block)

        return valid_neighbors

    def dfs_generation(self, current_block: Block) -> None:
        """
        Start at the Current Block, Check for Neighbors
        if any choose One Random, remove wall between current
        and that neighbor, mark it as checked and append block
        to the stack, if no neighbor found remove the
        last item (the current block) and access the last one [-1]
        this is BackTracking :)
        """
        if self.seed is not None:
            random.seed(self.seed)

        stack = [current_block]
        current_block.checked = True

        while stack:
            current_block = stack[-1]
            valid_neighbors = self.get_unvisited_neighbors(current_block)

            if not valid_neighbors:
                stack.pop()
                continue

            next_block = random.choice(valid_neighbors)

            self.remove_wall_between(current_block, next_block)

            next_block.checked = True
            stack.append(next_block)

    def random_loops(self, times: int = 81) -> None:
        """Add Random loops to make the Maze Imperfect"""
        candidates = []
        for y in range(self.height):
            for x in range(self.width):

                current_block = self.grid[y][x]
                if current_block.is_pattern:
                    continue

                neighbors = []
                if x + 1 < self.width and not self.grid[y][x + 1].is_pattern:
                    neighbors.append((x + 1, y))
                if y + 1 < self.height and not self.grid[y + 1][x].is_pattern:
                    neighbors.append((x, y + 1))
                if x - 1 >= 0 and not self.grid[y][x - 1].is_pattern:
                    neighbors.append((x - 1, y))
                if y - 1 >= 0 and not self.grid[y - 1][x].is_pattern:
                    neighbors.append((x, y - 1))

                if neighbors:
                    nx, ny = random.choice(neighbors)
                    neighbor_block = self.grid[ny][nx]
                    candidates.append((current_block, neighbor_block))

        random.shuffle(candidates)
        while candidates and times >= 0:
            current_block, next_block = candidates.pop(0)
            # Remove walls betweeb two blocks
            if not current_block.is_pattern and not next_block.is_pattern:
                self.remove_wall_between(current_block, next_block)
            times -= 1

    def hex_encoding(self) -> list:
        hex_lst = "0123456789ABCDEF"
        hex_output = []
        for y in range(self.height):
            output = []
            for x in range(self.width):
                value = 0
                block = self.grid[y][x]
                if block.has_wall("top"):
                    value += 1
                if block.has_wall("right"):
                    value += 2
                if block.has_wall("bottom"):
                    value += 4
                if block.has_wall("left"):
                    value += 8

                block_hex = hex_lst[value]
                output.append(block_hex)
            hex_output.append(output)

        return hex_output

    def path_direction(self) -> list:
        path = []
        solution = self.solution

        for i in range(len(solution) - 1):
            current = solution[i]
            nxt = solution[i + 1]

            if nxt.x > current.x:
                path.append("E")
            elif nxt.x < current.x:
                path.append("W")
            elif nxt.y > current.y:
                path.append("S")
            elif nxt.y < current.y:
                path.append("N")

        return path

    def visual(self, index: int) -> None:

        colors = [
            {
                "WALL": "\033[48;5;255m  \033[0m",
                "BLOCK": "\033[48;5;0m  \033[0m",
                "ENTRY": "\033[48;5;226m  \033[0m",
                "EXIT": "\033[48;5;196m  \033[0m",
                "PATTERN": "\033[48;5;57m  \033[0m",
                "PATH": "\033[48;5;21m  \033[0m"
            },
            {
                "WALL": "\033[48;5;236m  \033[0m",
                "BLOCK": "\033[48;5;213m  \033[0m",
                "ENTRY": "\033[48;5;82m  \033[0m",
                "EXIT": "\033[48;5;160m  \033[0m",
                "PATTERN": "\033[48;5;88m  \033[0m",
                "PATH": "\033[48;5;220m  \033[0m"
            },
            {
                "WALL": "\033[48;5;33m  \033[0m",
                "BLOCK": "\033[48;5;231m  \033[0m",
                "ENTRY": "\033[48;5;82m  \033[0m",
                "EXIT": "\033[48;5;202m  \033[0m",
                "PATTERN": "\033[48;5;161m  \033[0m",
                "PATH": "\033[48;5;0m  \033[0m"
            }
        ]

        ex, ey = self.entry.x, self.entry.y
        ox, oy = self.exit.x, self.exit.y

        block = colors[index].get("BLOCK")
        wall = colors[index].get("WALL")
        entry = colors[index].get("ENTRY")
        exit = colors[index].get("EXIT")
        pattern = colors[index].get("PATTERN")
        path = colors[index].get("PATH")
        for y in range(self.height):
            for x in range(self.width):
                b = self.grid[y][x]
                print(wall, end="")  # print the corner
                print(
                    wall if b.has_wall("top")
                    else block, end="")  # print the wal if existe
            print(wall)  # print the right most all blocks

            # Row 2: draw the "left" walls and the cell interior
            for x in range(self.width):
                b = self.grid[y][x]
                print(
                    wall if b.has_wall("left")
                    else block, end="")

                # cell interior (entry/exit/pattern/path)
                if (x, y) == (ex, ey):
                    print(entry, end="")
                elif (x, y) == (ox, oy):
                    print(exit, end="")
                elif b.is_pattern:
                    print(pattern, end="")
                elif self.show_path and b.is_path:
                    print(path, end="")
                else:
                    print(block, end="")

            # rightmost boundary: use the right wall of last cell
            last = self.grid[y][self.width - 1]
            print(
                wall if last.has_wall("right")
                else block)

        # Bottom boundary: draw the "bottom" walls of the last row
        for x in range(self.width):
            b = self.grid[self.height - 1][x]
            print(wall, end="")
            print(
                wall if b.has_wall("bottom")
                else block, end="")
        print(wall)

    def get_visited_neighbors(self, block: Block) -> list[Block]:
        visited_neighbors = []
        x, y = block.x, block.y

        potential_coords = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]

        for nx, ny in potential_coords:
            # 1. Check that nx , and ny insid the grid
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbor = self.grid[ny][nx]

                if neighbor.checked and not neighbor.is_pattern:
                    visited_neighbors.append(neighbor)

        return visited_neighbors

    def hunt_kill_generation(self) -> None:

        if self.seed is not None:
            random.seed(self.seed)

        current_block = self.grid[self.entry.y][self.entry.x]
        current_block.checked = True

        while current_block is not None:  # walk
            unvisited = self.get_unvisited_neighbors(current_block)

            if unvisited:  # if there's a neighbors
                neighbor = random.choice(unvisited)  # chose neighbor randomly
                self.remove_wall_between(current_block, neighbor)
                neighbor.checked = True
                current_block = neighbor  # move to the visited neighbor

            else:  # if get stock (no unvisited_neighbors)
                current_block = None
                # walk throgh the grid
                for y in range(self.height):

                    for x in range(self.width):
                        potential_block = self.grid[y][x]

                        if (
                                not potential_block.checked
                                and not potential_block.is_pattern
                        ):
                            visited_neighbors = self.get_visited_neighbors(
                                potential_block
                            )

                            if visited_neighbors:
                                neighbor = random.choice(visited_neighbors)
                                self.remove_wall_between(
                                    potential_block,
                                    neighbor
                                )

                                potential_block.checked = True
                                current_block = potential_block
                                # Break nested loops to restart WALK phase
                                break
                    if current_block:
                        break


class MazeSolver:

    def __init__(self, maze: MazeGenerator) -> None:
        self.height = maze.height
        self.width = maze.width

        self.entry = maze.entry
        self.exit = maze.exit

        self.grid = maze.grid
        self.solution = maze.solution

    def solve_maze(self, current_block: Block, exit_block: Block) -> None:
        """Solve the Maze using Breadth-First Search Algorithm"""

        blocks = deque([current_block])
        visited = set()
        familly_map: dict = {current_block: None}
        visited.add(current_block)

        while blocks:
            current_block = blocks.popleft()

            # stop if we reach the exit and save its block
            if (
                (current_block.x, current_block.y)
                == (exit_block.x, exit_block.y)
            ):
                break

            cx, cy = current_block.x, current_block.y
            neighbors = [(cx, cy - 1),
                         (cx, cy + 1),
                         (cx - 1, cy),
                         (cx + 1, cy)]

            for nx, ny in neighbors:
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    neighbor_block = self.grid[ny][nx]

                    if neighbor_block not in visited:
                        # check connected walls
                        if cx < nx:
                            if not current_block.has_wall(
                                "right"
                            ) and not neighbor_block.has_wall("left"):
                                blocks.append(neighbor_block)

                        elif cx > nx:
                            if not current_block.has_wall(
                                "left"
                            ) and not neighbor_block.has_wall("right"):
                                blocks.append(neighbor_block)

                        elif cy > ny:
                            if not current_block.has_wall(
                                "top"
                            ) and not neighbor_block.has_wall("bottom"):
                                blocks.append(neighbor_block)

                        elif cy < ny:
                            if not current_block.has_wall(
                                "bottom"
                            ) and not neighbor_block.has_wall("top"):
                                blocks.append(neighbor_block)
                        else:
                            continue

                        if neighbor_block in blocks:
                            visited.add(neighbor_block)
                            familly_map[neighbor_block] = current_block

        # trace back the path
        key_block = self.grid[exit_block.y][exit_block.x]

        while key_block is not None:
            self.solution.append(key_block)
            key_block = familly_map.get(key_block)

        self.solution.reverse()
        for block in self.solution:
            block.is_path = True

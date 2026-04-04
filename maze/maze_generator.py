import random
from maze.block import Block


class MazeGenerator:

    def __init__(self, config: dict):
        """
        Take the config dict as an Attribute
        while creating maze instance ,
        extract height and width
        """

        self.height = config["HEIGHT"]
        self.width = config["WIDTH"]

        self.entry = config["ENTRY"]
        self.exit = config["EXIT"]

        self.seed = config["SEED"]

        self.grid = []
        self.solution = []

    def grid_builder(self) -> None:
        """
        Build the Grid System Based On
        the HEIGHT &&& WIDTH from Config File
        """
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(Block(x, y))
            self.grid.append(row)

    def remove_wall_between(self, a: Block, b: Block):

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
            if 0 <= dy < self.height and 0 <= dx < self.width:
                self.grid[dy][dx].is_pattern = True

        for dy, dx in two:
            if 0 <= dy < self.height and 0 <= dx < self.width:
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

    def hunt_kill_generation():
        pass

    def random_loops(self) -> None:
        """Add Random loops to make the Maze Imperfect"""

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

                    # Remove walls betweeb two blocks
                    self.remove_wall_between(current_block, neighbor_block)

    def hex_encoding(self) -> list:
        hex_lst = "0123456789ABCDEF"
        hex_output = []
        for row in range(self.height):
            output = []
            for col in range(self.width):
                value = 0
                block = self.grid[row][col]
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

    def visual(self) -> None:
        # Background-color "pixels" (two spaces)
        WHITE = "\033[48;5;250m  \033[0m"  # wall color (bright)
        BLACK = "\033[48;5;0m  \033[0m"    # passage color
        GREEN = "\033[48;5;46m  \033[0m"   # entry
        RED = "\033[48;5;196m  \033[0m"  # exit
        BORDEAUX = "\033[48;5;88m  \033[0m"    # pattern (optional)

        if not self.grid:
            print("(maze grid is empty)")
            return

        ex, ey = self.entry.x, self.entry.y
        ox, oy = self.exit.x, self.exit.y

        for y in range(self.height):
            # Row 1: draw the "top" walls of each cell + corner walls
            for x in range(self.width):
                b = self.grid[y][x]
                print(WHITE, end="")  # the left corner / pillar
                print(WHITE if b.has_wall("top") else BLACK, end="")
            print(WHITE)  # rightmost corner

            # Row 2: draw the "left" walls and the cell interior
            for x in range(self.width):
                b = self.grid[y][x]
                print(WHITE if b.has_wall("left") else BLACK, end="")

                # cell interior (entry/exit/pattern/path)
                if (x, y) == (ex, ey):
                    print(GREEN, end="")
                elif (x, y) == (ox, oy):
                    print(RED, end="")
                elif getattr(b, "is_pattern", False):
                    print(BORDEAUX, end="")
                else:
                    print(BLACK, end="")

            # rightmost boundary: use the right wall of last cell
            last = self.grid[y][self.width - 1]
            print(WHITE if last.has_wall("right") else BLACK)

        # Bottom boundary: draw the "bottom" walls of the last row
        for x in range(self.width):
            b = self.grid[self.height - 1][x]
            print(WHITE, end="")
            print(WHITE if b.has_wall("bottom") else BLACK, end="")
        print(WHITE)

    def re_gen_maze() -> None:
        ...

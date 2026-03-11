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
        self.perfect = config["PERFECT"]

        self.entry = config["ENTRY"]
        self.exit = config["EXIT"]

        self.seed = config["SEED"]
        self.pattern = config["PATTERN"]

        self.grid = []
        self.solution = []


    def generate_all(self, start_block):
        self.ft_pattern()
        self.maze_algo(start_block)

        if not self.perfect:
            self.random_loops()



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

        # number = self.pattern
        # digits = []
        # while number > 0:
        #     digits.append(number % 10)
        #     number //= 10
        # digits.reverse()
        
        four = [
            (cy-2, cx-3),
            (cy-1, cx-3),
            (cy, cx-1),
            (cy, cx-2),
            (cy, cx-3),
            (cy, cx-1),
            (cy+1, cx-1),
            (cy+2, cx-1)
        ]
        
        two = [
            (cy+2, cx+1),
            (cy+2, cx+2),
            (cy-1, cx+3),
            (cy+2, cx+3),
            (cy, cx+1),
            (cy, cx+2),
            (cy, cx+3),
            (cy+1, cx+1),
            (cy-2, cx+1),
            (cy-2, cx+2),
            (cy-2, cx+3)
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

        neighbors = [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]
        
        # loop over Neighbors & Add valid ones that hasn't checked yet
        for n in neighbors:
            nx, ny = n
            if 0 <= nx < self.width and 0 <= ny < self.height:
                this_block = self.grid[ny][nx]

                if not this_block.checked and not this_block.is_pattern:
                    valid_neighbors.append(this_block)

        return valid_neighbors



    def maze_algo(self, current_block: Block) -> None:
        
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



    def random_loops(self) -> None:
        """ Add Random loops to make the Maze Imperfect """
        
        for y in range(self.height):
            for x in range(self.width):

                current_block = self.grid[y][x]
                if current_block.is_pattern:
                    continue

                neighbors = []
                if x + 1 < self.width and not self.grid[y][x+1].is_pattern:
                    neighbors.append((x+1, y))
                if y + 1 < self.height and not self.grid[y+1][x].is_pattern:
                    neighbors.append((x, y+1))
                if x - 1 >= 0 and not self.grid[y][x-1].is_pattern:
                    neighbors.append((x-1, y))
                if y - 1 >= 0 and not self.grid[y-1][x].is_pattern:
                    neighbors.append((x, y-1))

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
                if block.has_wall("top"): value += 1
                if block.has_wall("right"): value += 2
                if block.has_wall("bottom"): value += 4
                if block.has_wall("left"): value += 8

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



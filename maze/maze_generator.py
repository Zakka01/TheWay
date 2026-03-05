import random

class Block:
    def __init__(self, x: int, y: int):

        """
            Initialize the attributes : 
            x, y => ofc the coordinates, 
            walls => if the block closed or not
            checked => if the block already visited or not
            ... 
        """
        self.x = x
        self.y = y
        self.walls = {
            "top": True,
            "bottom": True,
            "left": True,
            "right": True
        }
        self.checked = False



    def has_wall(self, direction: str) -> bool:

        """ 
            check if block has wall in the given direction
            and return True if yes , otherwise False
        """
        if self.walls[direction] == True:
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
        self.grid = []
        self.height = config["HEIGHT"]
        self.width = config["WIDTH"]
        self.seed = config["SEED"]



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



    def check_around(self, block: Block) -> list:
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
                if not this_block.checked:
                    valid_neighbors.append(this_block)

        return valid_neighbors



    def generate(self, current_block: Block):
        
        """
            Start at the Current Block, Check for Neighbors
            if any choose One Random, remove wall between current 
            and that neighbor, mark it as checked call the function 
            Recusively for that Neighbor as Param
        """
        random.seed(self.seed)

        stack = [current_block]
        current_block.checked = True

        while stack:
            current_block = stack[-1]
            valid_neighbors = self.check_around(current_block)

            if not valid_neighbors:
                stack.pop()
                continue
            
            next_block = random.choice(valid_neighbors)

            cx, cy = current_block.x, current_block.y
            nx, ny = next_block.x, next_block.y
            if cx < nx:
                current_block.pop_wall("right")
                next_block.pop_wall("left")
            elif cx > nx:
                current_block.pop_wall("left")
                next_block.pop_wall("right")
            elif cy > ny:
                current_block.pop_wall("top")
                next_block.pop_wall("bottom")
            elif cy < ny:
                current_block.pop_wall("bottom")
                next_block.pop_wall("top")

            next_block.checked = True
            stack.append(next_block)



    def hex_encoding(self) -> list:
        hex_lst = "0123456789ABCDEF"
        hex_output = []
        for col in range(self.width):
            row_output = []
            for row in range(self.height):
                value = 0
                block = self.grid[row][col]
                if block.has_wall("top"): value += 1
                if block.has_wall("right"): value += 2
                if block.has_wall("bottom"): value += 4
                if block.has_wall("left"): value += 8

                block_hex = hex_lst[value]
                row_output.append(block_hex)
            hex_output.append(row_output)

        return hex_output



    # Just a small visualizer to see the generated maze 
    def print_maze(self):
        top_row = "o"

        for x in range(self.width):
            if self.grid[0][x].walls["top"]:
                top_row += "---+"
            else:
                top_row += "   +"
        print(top_row)

        for y in range(self.height):
            row_top = "|"
            row_bottom = "+"

            for x in range(self.width):
                block = self.grid[y][x]

                # cell space
                row_top += "   "

                # right wall
                if block.walls["right"]:
                    row_top += "|"
                else:
                    row_top += " "

                # bottom wall
                if block.walls["bottom"]:
                    row_bottom += "---+"
                else:
                    row_bottom += "   +"

            print(row_top)
            print(row_bottom)
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


class MazeGen:
    """
        The Main Maze Generator Class
    """

    def __init__(self, config: dict):
        """
            Take the config dict as an Attribute 
            while creating maze instance ,
            extract height and width
        """  
        self.grid = []
        self.height = config["HEIGHT"]
        self.width = config["WIDTH"]



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



    def check_around(self, block: Block):
        """
            check the 4 possible neighbors
            while x & y are the coordinates
        """
        valid_neighbors = []
        x, y = block.x, block.y

        top = (x, y-1)
        bottom = (x, y+1)
        left = (x-1, y)
        right = (x+1, y)
        
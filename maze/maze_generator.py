class Block:
    def __init__(self, x: int, y: int):

        """
            Initialize the attributes : 
            x, y => ofc the coordinates, 
            walls => if the block closed or not
            checked => if the block already visited or not 
        """

        self.x = x
        self.y = y
        self.walls = {
            "n": True,
            "s": True,
            "e": True,
            "w": True
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


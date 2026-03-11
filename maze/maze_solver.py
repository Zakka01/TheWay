from maze.maze_generator import MazeGenerator
from maze.block import Block
from collections import deque



class MazeSolver():

    def __init__(self, maze):
        self.height = maze.height
        self.width = maze.width

        self.entry = maze.entry
        self.exit = maze.exit

        self.grid = maze.grid
        self.solution = maze.solution
        
        
        
    def is_connected(self, current_block, neighbor_block):
        cx, cy = current_block.x, current_block.y
        nx, ny = neighbor_block.x, neighbor_block.y

        if cx < nx:
            return not current_block.has_wall("right") and not neighbor_block.has_wall("left")

        if cx > nx:
            return not current_block.has_wall("left") and not neighbor_block.has_wall("right")

        if cy > ny:
            return not current_block.has_wall("top") and not neighbor_block.has_wall("bottom")

        if cy < ny:
            return not current_block.has_wall("bottom") and not neighbor_block.has_wall("top")

        return False



    def build_solution(self, familly_map, exit_block):

        #trace back the path
        key = self.grid[exit_block.y][exit_block.x]

        while key is not None:
            self.solution.append(key)
            key = familly_map.get(key)

        self.solution.reverse()
        for block in self.solution:
            block.is_path = True



    def solve_maze(self, current_block: Block, exit_block: Block) -> None:

        """ Solve the Maze using Breadth-First Search Algorithm """

        blocks = deque([current_block])
        visited = set()
        familly_map = {current_block: None}
        visited.add(current_block)

        while blocks:
            current_block = blocks.popleft()
            
            # stop if we reach the exit and save its block
            if (current_block.x, current_block.y) == (exit_block.x, exit_block.y):
                break

            cx, cy = current_block.x, current_block.y
            neighbors = [(cx, cy-1), (cx, cy+1), (cx-1, cy), (cx+1, cy)]

            for nx, ny in neighbors:
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    neighbor_block = self.grid[ny][nx]

                    if neighbor_block in visited:
                        continue
                    
                    # check connected walls 
                    if self.is_connected(current_block, neighbor_block):
                        blocks.append(neighbor_block) 
                        visited.add(neighbor_block)
                        familly_map[neighbor_block] = current_block

        self.build_solution(familly_map, exit_block)


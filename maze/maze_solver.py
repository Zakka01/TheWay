from maze.block import Block
from collections import deque


class MazeSolver():

    def __init__(self, maze):
        self.maze = maze
        self.height = maze.height
        self.width = maze.width

        self.entry = maze.entry
        self.exit = maze.exit

        self.grid = maze.grid
        self.solution = maze.solution
        
        self.queue = deque()
        self.visited = set()
        self.family_map = {}
        self.exit_block = None
        self.solving = True

        self.show_visited = True


    def reset_solve(self) -> None:
        self.queue = deque()
        self.visited = set()
        self.family_map = {}
        
        self.grid = self.maze.grid
        x, y = self.entry
        ex, ey = self.exit

        start_block = self.grid[y][x]
        exit_block = self.grid[ey][ex]
        
        self.start_solving(start_block, exit_block)
        
        
        
    def is_connected(self, current_block, neighbor_block) -> bool:
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



    def build_solution(self, familly_map, exit_block) -> None:

        key = self.grid[exit_block.y][exit_block.x]

        while key is not None:
            self.solution.append(key)
            key = familly_map.get(key)

        self.solution.reverse()


    
    def start_solving(self, start_block, exit_block) -> None:

        self.queue = deque([start_block])
        self.visited = {start_block}
        self.family_map = {start_block: None}

        self.exit_block = exit_block



    def solve_maze(self) -> bool:

        """ Solve the Maze using Breadth-First Search Algorithm """

        if not self.queue:
            self.solving = False
            return False

        current_block = self.queue.popleft()
        current_block.visited_by_bfs = True
        
        # stop if we reach the exit and save its block
        if current_block == self.exit_block:
            self.build_solution(self.family_map, self.exit_block)
            self.solving = False
        
            for row in self.grid:
                for block in row:
                    block.visited_by_bfs = False

            return False


        cx, cy = current_block.x, current_block.y
        neighbors = [(cx, cy-1), (cx, cy+1), (cx-1, cy), (cx+1, cy)]

        for nx, ny in neighbors:
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbor_block = self.grid[ny][nx]

                if neighbor_block in self.visited:
                    continue
                
                # check connected walls 
                if self.is_connected(current_block, neighbor_block):
                    self.queue.append(neighbor_block) 
                    self.visited.add(neighbor_block)
                    self.family_map[neighbor_block] = current_block
        return True

import pygame

class MazeRenderer:

    def __init__(self, maze):
        pygame.init()
        
        self.maze = maze
        self.block_size = 40
        self.window_height = maze.height * self.block_size
        self.window_width = maze.width * self.block_size

        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height)
        )
        pygame.display.set_caption("Do Not Get Lost")
        
        self.bg_color   = (0, 0, 0)
        self.block_color   = (0, 0, 40)
        self.wall_color = (255, 255, 255)

        self.path_color = (0, 255, 20)
        self.entry_color= (0, 0, 255)
        self.exit_color = (255, 0, 0)



    def run(self) -> None:

        running = True
        while running:

            self.screen.fill(self.bg_color)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
            
            self.draw_maze()
            pygame.display.flip()

        pygame.quit()



    def draw_maze(self) -> None:

        for row in self.maze.grid:
            for block in row:
                px = block.x * self.block_size
                py = block.y * self.block_size

                self.draw_block(px, py)

                if block.is_path:
                    self.draw_path(px, py)
                if block == self.maze.entry:
                    self.draw_entry(px, py)
                if block == self.maze.exit:
                    self.draw_exit(px, py)

                self.draw_walls(block, px, py)



    def draw_walls(self, block, px, py) -> None:
        
        if block.has_wall("top"):
            pygame.draw.line(
                self.screen,
                self.wall_color,
                (px, py),
                (px + self.block_size, py),
                4
            )

        if block.has_wall("right"):
            pygame.draw.line(
                self.screen,
                self.wall_color,
                (px + self.block_size, py),
                (px + self.block_size, py + self.block_size),
                7
            )

        if block.has_wall("bottom"):
            pygame.draw.line(
                self.screen, 
                self.wall_color, 
                (px, py + self.block_size), 
                (px + self.block_size, py + self.block_size), 
                4
            )

        if block.has_wall("left"):
            pygame.draw.line(
                self.screen,
                self.wall_color,
                (px, py),
                (px, py + self.block_size), 
                7
            )



    def draw_block(self, px, py) -> None:

        pygame.draw.rect(
            self.screen,
            self.block_color,
            (px, py, self.block_size, self.block_size)
        )



    def draw_path(self, px, py) -> None:

        pygame.draw.rect(
            self.screen,
            self.path_color,
            (px + 10, py + 10, self.block_size - 20, self.block_size - 20)
        )



    def draw_entry(self, px, py) -> None:

        pygame.draw.rect(
            self.screen,
            self.entry_color,
            (px + 6, py + 6, self.block_size - 12, self.block_size - 12)
        )



    def draw_exit(self, px, py) -> None:

        pygame.draw.rect(
            self.screen,
            self.exit_color,
            (px + 6, py + 6, self.block_size - 12, self.block_size - 12)
        )

import pygame

class MazeRenderer:
    def __init__(self, maze):
        pygame.init()
        
        self.maze = maze
        self.block_size = 40
        self.wall_thickness = 8
        self.window_height = maze.height * self.block_size
        self.window_width = maze.width * self.block_size

        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height)
        )
        pygame.display.set_caption("Do Not Get Lost - Forest Maze")

        # Colors
        self.bg_color = (30, 30, 30)
        self.path_color = (180, 140, 50)
        
        # Load textures
        self.grass_texture = pygame.transform.scale(
            pygame.image.load("assets/grass_texture.png"), 
            (self.block_size, self.block_size)
        )
        self.tree_texture = pygame.transform.scale(
            pygame.image.load("assets/tree_texture.png"),
            (self.block_size, self.block_size)
        )
        self.path_texture = pygame.transform.scale(
            pygame.image.load("assets/path_texture.png"),
            (self.block_size - 20, self.block_size - 20)
        )
        self.stone_texture = pygame.transform.scale(
            pygame.image.load("assets/stone_texture.png"),
            (self.block_size, self.block_size)
        )
        self.player = pygame.transform.scale(
            pygame.image.load("assets/farmer.jpg"),
            (self.block_size, self.block_size)
        )
        self.entry_texture = pygame.transform.scale(
            pygame.image.load("assets/entry.png"),
            (self.block_size - 10, self.block_size - 10)
        )
        self.exit_texture = pygame.transform.scale(
            pygame.image.load("assets/exit.png"),
            (self.block_size - 10, self.block_size - 10)
        )




    def rendering(self):
        running = True
        while running:
            self.screen.fill(self.bg_color)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.draw_maze()
            pygame.display.flip()

        pygame.quit()




    def draw_maze(self):
        for row in self.maze.grid:
            for block in row:
                px = block.x * self.block_size
                py = block.y * self.block_size

                # Draw grass base
                self.draw_block(px, py)

                # Draw path tiles
                if block.is_path:
                    self.draw_path(px, py)

                # Draw pattern blocks
                if block.is_pattern:
                    self.draw_pattern(px, py)

                # Entry / Exit
                if block == self.maze.entry:
                    self.draw_entry(px, py)
                if block == self.maze.exit:
                    self.draw_exit(px, py)

                # Walls with tree textures
                self.draw_walls(block, px, py)




    def draw_block(self, px, py):
        self.screen.blit(self.grass_texture, (px, py))




    def draw_walls(self, block, px, py):
        t = self.tree_texture
        s = self.block_size
        if block.is_pattern:
            w = self.wall_thickness - 7.5
        else:
            w = self.wall_thickness

        if block.has_wall("top"):
            self.screen.blit(pygame.transform.scale(t, (s, w)), (px, py))
        if block.has_wall("right"):
            self.screen.blit(pygame.transform.rotate(pygame.transform.scale(t, (w, s)), 0), (px + s - w, py))
        if block.has_wall("bottom"):
            self.screen.blit(pygame.transform.scale(t, (s, w)), (px, py + s - w))
        if block.has_wall("left"):
            self.screen.blit(pygame.transform.rotate(pygame.transform.scale(t, (w, s)), 0), (px, py))




    def draw_path(self, px, py):
        self.screen.blit(self.path_texture, (px + 10, py + 10))

    def draw_pattern(self, px, py):
        self.screen.blit(self.stone_texture, (px, py))

    def draw_entry(self, px, py):
        self.screen.blit(self.entry_texture, (px + 5, py + 5))

    def draw_exit(self, px, py):
        self.screen.blit(self.exit_texture, (px + 5, py + 5))
import os
import pygame
import random
from maze.maze_generator import MazeGenerator
from maze.maze_solver import MazeSolver
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"


class MazeRenderer:

    def __init__(self, maze: MazeGenerator, solve: MazeSolver):
        pygame.init()

        self.maze = maze
        self.solve = solve
        self.toggle_path = True
        self.maze_design = 0

        self.player_idx = 0
        self.block_size = 30
        self.wall_thickness = 3
        self.menu_height = 30

        self.window_height = (
            maze.height * self.block_size + self.menu_height + 10
        )  # 10 for padding
        self.window_width = maze.width * self.block_size + 10  # 10 for padding

        self.screen = pygame.display.set_mode((self.window_width,
                                               self.window_height))
        pygame.display.set_caption("A-Maze-ing")

        self.clock = pygame.time.Clock()

        self.bg_color = (141, 153, 150)
        self.path_color = (209, 187, 145)

        self.grass_texture = pygame.transform.scale(
            pygame.image.load("assets/grass_texture.png"),
            (self.block_size, self.block_size),
        )
        self.tree_texture = pygame.transform.scale(
            pygame.image.load("assets/tree_texture.png"),
            (self.block_size, self.block_size),
        )
        self.path_texture = pygame.transform.scale(
            pygame.image.load("assets/path_texture.png"),
            (self.block_size - 20, self.block_size - 20),
        )
        self.ft_texture = pygame.transform.scale(
            pygame.image.load("assets/stone_texture.png"),
            (self.block_size, self.block_size),
        )
        self.player = pygame.transform.scale(
            pygame.image.load("assets/player.png"), (self.block_size,
                                                     self.block_size)
        )
        self.entry_texture = pygame.transform.scale(
            pygame.image.load("assets/entry.png"),
            (self.block_size - 10, self.block_size - 10),
        )
        self.exit_texture = pygame.transform.scale(
            pygame.image.load("assets/exit.png"),
            (self.block_size - 10, self.block_size - 10),
        )
        self.stone_bg = pygame.transform.scale(
            pygame.image.load("assets/stone_background.png"),
            (self.block_size, self.block_size),
        )
        self.stone_wall = pygame.transform.scale(
            pygame.image.load("assets/stone_wall.png"),
            (self.block_size, self.block_size),
        )
        self.ft_texture2 = pygame.transform.scale(
            pygame.image.load("assets/ft_background.png"),
            (self.block_size, self.block_size),
        )
        self.entry_texture2 = pygame.transform.scale(
            pygame.image.load("assets/blackhole_entry.png"),
            (self.block_size - 10, self.block_size - 10),
        )
        self.exit_texture2 = pygame.transform.scale(
            pygame.image.load("assets/exit_gold.png"),
            (self.block_size - 10, self.block_size - 10),
        )

    def draw_menu(self):
        font = pygame.font.SysFont(None, 24)
        menu_options = [
            "[ 1 ]   Re-generate",
            "[ 2 ]   Toggle Path",
            "[ 3 ]   Colors",
            "[ 4 ]   Quit",
        ]
        x_offset = 10
        y_pos = self.maze.height * self.block_size + 15

        for option in menu_options:
            img = font.render(option, True, (0, 0, 0))
            self.screen.blit(img, (x_offset, y_pos))
            x_offset += img.get_width() + 40

    def rendering(self):
        running = True
        generating = True

        while running:
            self.screen.fill(self.bg_color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    # re-gen maze
                    if event.key == pygame.K_1:
                        seed = random.randint(1, 1000)
                        self.maze.reset_maze(seed)
                        self.solve.reset_solve()
                        self.player_idx = 0
                        generating = True

                    # toggle-path
                    if event.key == pygame.K_2:
                        self.toggle_path = not self.toggle_path

                    # change design
                    if event.key == pygame.K_3:
                        self.maze_design += 1

                    # Quit
                    if event.key == pygame.K_4:
                        running = False

            # Generate maze, step on each call
            if generating:
                generating = self.maze.maze_generation_dfs()
                self.clock.tick(120)

            # solve maze, block on each call
            elif self.solve.solving:
                still_solve = self.solve.solve_maze()
                if not still_solve:
                    self.solve.solving = False
                    self.player_idx = 0

            # player move
            elif self.player_idx < len(self.solve.solution):
                self.clock.tick(10)

                block = self.solve.solution[self.player_idx]
                block.is_path = True

                self.player_idx += 1

            self.draw_in_maze()
            self.draw_player()
            self.draw_menu()
            pygame.display.flip()

        pygame.quit()

    def draw_in_maze(self):
        for row in self.maze.grid:

            for block in row:

                px = block.x * self.block_size + 5  # 5 for padding
                py = block.y * self.block_size + 5  # 5 for padding

                self.draw_block(px, py)

                if block.is_pattern:
                    self.draw_pattern(px, py)

                self.draw_walls(block, px, py)

                if self.toggle_path and block.is_path:
                    self.draw_path(block, px, py)

                if block.visited_by_bfs:
                    pygame.draw.rect(
                        self.screen,
                        (80, 80, 120),
                        (px, py, self.block_size, self.block_size),
                    )

                if (
                    block == self.maze.current_block
                    and (block.x, block.y) != self.maze.entry
                ):
                    self.draw_current(px, py)

                if (block.x, block.y) == self.maze.entry:
                    self.draw_entry(px, py)
                if (block.x, block.y) == self.maze.exit:
                    self.draw_exit(px, py)

    def draw_block(self, px, py):
        if self.maze_design % 2 == 1:
            block_background = self.grass_texture
        elif self.maze_design % 2 == 0:
            block_background = self.stone_bg
        self.screen.blit(block_background, (px, py))

    def draw_current(self, px, py):
        if self.maze_design % 2 == 1:
            current_color = (245, 245, 220)
        elif self.maze_design % 2 == 0:
            current_color = (244, 244, 244)
        padding = 4
        pygame.draw.rect(
            self.screen,
            current_color,
            (
                px + padding,
                py + padding,
                self.block_size - padding * 2,
                self.block_size - padding * 2,
            ),
            3,
        )

    def draw_walls(self, block, px, py):

        if self.maze_design % 2 == 1:
            texture = self.tree_texture
        elif self.maze_design % 2 == 0:
            texture = self.stone_wall

        size = self.block_size
        if block.is_pattern:
            width = 2
        else:
            width = self.wall_thickness

        if block.has_wall("top"):
            self.screen.blit(pygame.transform.scale(texture, (size, width)),
                             (px, py))
        if block.has_wall("right"):
            self.screen.blit(
                pygame.transform.rotate(
                    pygame.transform.scale(texture, (width, size)), 0
                ),
                (px + size - width, py),
            )
        if block.has_wall("bottom"):
            self.screen.blit(
                pygame.transform.scale(texture, (size, width)),
                (px, py + size - width)
            )
        if block.has_wall("left"):
            self.screen.blit(
                pygame.transform.rotate(
                    pygame.transform.scale(texture, (width, size)), 0
                ),
                (px, py),
            )

    def draw_player(self) -> None:
        if self.player_idx == 0 or self.player_idx >= len(self.solve.solution):
            return

        block = self.solve.solution[self.player_idx - 1]

        px = block.x * self.block_size
        py = block.y * self.block_size

        self.screen.blit(self.player, (px, py))

    def draw_path(self, block, px, py):

        cx = px + self.block_size // 2
        cy = py + self.block_size // 2
        thickness = 6

        x = block.x
        y = block.y

        # top
        if y > 0 and not block.has_wall("top"):
            neighbor = self.maze.grid[y - 1][x]
            if neighbor.is_path:
                pygame.draw.line(
                    self.screen,
                    self.path_color,
                    (cx, cy),
                    (cx, cy - self.block_size),
                    thickness,
                )

        # right
        if x < self.maze.width - 1 and not block.has_wall("right"):
            neighbor = self.maze.grid[y][x + 1]
            if neighbor.is_path:
                pygame.draw.line(
                    self.screen,
                    self.path_color,
                    (cx, cy),
                    (cx + self.block_size, cy),
                    thickness,
                )

        # bottom
        if y < self.maze.height - 1 and not block.has_wall("bottom"):
            neighbor = self.maze.grid[y + 1][x]
            if neighbor.is_path:
                pygame.draw.line(
                    self.screen,
                    self.path_color,
                    (cx, cy),
                    (cx, cy + self.block_size),
                    thickness,
                )

        # left
        if x > 0 and not block.has_wall("left"):
            neighbor = self.maze.grid[y][x - 1]
            if neighbor.is_path:
                pygame.draw.line(
                    self.screen,
                    self.path_color,
                    (cx, cy),
                    (cx - self.block_size, cy),
                    thickness,
                )

    def draw_pattern(self, px, py):
        if self.maze_design % 2 == 1:
            ft_txt = self.ft_texture
        elif self.maze_design % 2 == 0:
            ft_txt = self.ft_texture2

        self.screen.blit(ft_txt, (px, py))

    def draw_entry(self, px, py):
        if self.maze_design % 2 == 1:
            entry_txt = self.entry_texture
        elif self.maze_design % 2 == 0:
            entry_txt = self.entry_texture2
        padding = 5
        self.screen.blit(entry_txt, (px + padding, py + padding))

    def draw_exit(self, px, py):
        if self.maze_design % 2 == 1:
            exit_txt = self.exit_texture
        elif self.maze_design % 2 == 0:
            exit_txt = self.exit_texture2
        padding = 3
        self.screen.blit(exit_txt, (px + padding, py + padding))

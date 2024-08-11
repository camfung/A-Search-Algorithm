from dataStructures import Grid, Agent, Spot, AgentsHandler
import pygame
import random
from typing import List
from MakeMaze import make_maze_recursion


class Direction:
    HORIZONTAL = 1
    VERTICAL = 2


class ShowSim:
    update_agents_event = pygame.USEREVENT
    clock = pygame.time.Clock()

    def __init__(self, grid: Grid, agents_handler: AgentsHandler, cell_size=20, outline_width=1):
        self.grid = grid
        self.cell_size = cell_size
        self.outline_width = outline_width
        self.width = grid.width * cell_size
        self.height = grid.height * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.agents_handler = agents_handler
        self.start = False
        self.mouse_held = False
        self.flip_deplay = 200
        self.last_tile_flipped = (-1, -1)
        self.brush_radius = 1

        pygame.display.set_caption("Grid Display")
        pygame.time.set_timer(ShowSim.update_agents_event, 50)

    def draw_grid(self):
        self.screen.fill((255, 255, 255))  # Fill the screen with white

        for row in range(self.grid.height):
            for col in range(self.grid.width):
                spot = self.grid[row][col]
                rect_x = col * self.cell_size
                rect_y = row * self.cell_size
                color = (0, 0, 255) if spot.is_wall else (255, 255, 255)
                pygame.draw.rect(
                    self.screen, color,
                    (rect_x, rect_y, self.cell_size, self.cell_size)
                )
                pygame.draw.rect(
                    self.screen, (0, 0, 0),
                    (rect_x, rect_y, self.cell_size, self.cell_size),
                    self.outline_width
                )

    def draw_path(self, path, color=(255, 0, 0), line_width=3):
        """
        Draws a line connecting each node in the given path.

        :param path: List of tuples where each tuple is a (row, col) representing a node in the path.
        :param color: The color of the line to be drawn.
        :param line_width: The width of the line.
        """
        # Convert grid coordinates to pixel coordinates
        pixel_path = [(col * self.cell_size + self.cell_size // 2,
                       row * self.cell_size + self.cell_size // 2)
                      for row, col in path]

        # Draw lines between each consecutive node
        if len(pixel_path) > 1:
            for i in range(len(pixel_path) - 1):
                pygame.draw.line(self.screen, color,
                                 pixel_path[i], pixel_path[i + 1], line_width)

    def draw_agents(self):
        for agent in self.agents_handler.agents:
            row = agent.row
            col = agent.col
            rect_x = col * self.cell_size
            rect_y = row * self.cell_size
            pygame.draw.rect(
                self.screen, agent.color,
                (rect_x, rect_y, self.cell_size, self.cell_size),
                0
            )

    def get_grid_position(self, pos):
        x, y = pos
        col = x // self.cell_size
        row = y // self.cell_size
        return row, col

    def set_is_wall(self, pos):
        center_row = pos[0]
        center_col = pos[1]
        start = (center_row - self.brush_radius,
                 center_col - self.brush_radius)
        end = (center_row + self.brush_radius, center_col + self.brush_radius)
        for row in range(start[0], end[0]):
            for col in range(start[1], end[1]):
                try:
                    grid[row][col].is_wall = True
                except IndexError:
                    pass

    def set_not_is_wall(self, pos):
        center_row = pos[0]
        center_col = pos[1]
        start = (center_row - self.brush_radius,
                 center_col - self.brush_radius)
        end = (center_row + self.brush_radius, center_col + self.brush_radius)
        for row in range(start[0], end[0]):
            for col in range(start[1], end[1]):
                grid[row][col].is_wall = False

    def draw_agents_paths(self):
        for agent in self.agents_handler.agents:
            self.draw_path(agent.route_travelled)

    def run(self):
        running = True
        while running:
            current_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == self.update_agents_event and self.start:
                    self.agents_handler.update_agents()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.agents_handler.calculate_agents_routes()
                        self.start = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.mouse_held = True
                        pos = pygame.mouse.get_pos()
                        row, col = self.get_grid_position(pos)
                        if not self.start and self.last_tile_flipped != (row, col):
                            self.set_not_is_wall((row, col))
                            self.last_tile_flipped = (row, col)
                    elif event.button == 3:
                        if not self.start and self.last_tile_flipped != (row, col):
                            self.set_is_wall((row, col))
                            self.last_tile_flipped = (row, col)

                elif event.type == pygame.MOUSEMOTION:
                    if self.mouse_held:
                        pos = pygame.mouse.get_pos()
                        row, col = self.get_grid_position(pos)
                        if not self.start and self.last_tile_flipped != (row, col) and pygame.mouse.get_pressed()[0]:
                            self.set_not_is_wall((row, col))
                            self.last_tile_flipped = (row, col)

                        elif not self.start and self.last_tile_flipped != (row, col) and pygame.mouse.get_pressed()[1]:
                            self.set_not_is_wall((row, col))
                            self.last_tile_flipped = (row, col)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.mouse_held = False

            self.draw_grid()
            self.draw_agents_paths()
            self.draw_agents()
            pygame.display.flip()

            ShowSim.clock.tick(60)


pygame.quit()


# Example usage:
if __name__ == "__main__":
    grid_width, grid_height = 60, 60
    # Create a sample grid
    # grid = make_maze_recursion(grid_width, grid_height)
    grid = Grid(width=grid_width, height=grid_height,
                border_walls=True, fill=True)

    agents = [
        Agent(1, 1, grid_width-2, grid_height-2),
        # Agent(grid_width-2, 1, 1, grid_width-2)
    ]

    agents_handler = AgentsHandler(agents=agents, grid=grid)

    # Create and run the ShowGrid
    show_grid = ShowSim(grid, agents_handler)
    show_grid.run()

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

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == self.update_agents_event and self.start:
                    self.agents_handler.update_agents()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.start = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.mouse_held = True
                        pos = pygame.mouse.get_pos()
                        row, col = self.get_grid_position(pos)
                        print(f"Mouse Clicked at Row: {row}, Column: {col}")

                elif event.type == pygame.MOUSEMOTION:
                    if self.mouse_held:
                        pos = pygame.mouse.get_pos()
                        row, col = self.get_grid_position(pos)
                        print(
                            f"Mouse Held and Moved to Row: {row}, Column: {col}")

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.mouse_held = False

            self.draw_grid()
            self.draw_agents()
            pygame.display.flip()

            ShowSim.clock.tick(60)


pygame.quit()


# Example usage:
if __name__ == "__main__":
    grid_width, grid_height = 60, 60
    # Create a sample grid
    grid = make_maze_recursion(grid_width, grid_height)

    agent = Agent(1, 1, grid_width-2, grid_height-2)
    agent2 = Agent(58, 1, 1, 58)

    pattern = agent.astar(grid)
    agent.route_planned = pattern
    print("pattern: ", pattern)
    agents_handler = AgentsHandler(agents=[agent, agent2], grid=grid)

    # Create and run the ShowGrid
    show_grid = ShowSim(grid, agents_handler)
    show_grid.run()

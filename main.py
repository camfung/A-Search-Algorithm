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

    def __init__(self, grid: Grid, agents: List[Agent], cell_size=20, outline_width=1):
        self.grid = grid
        self.agents = agents
        self.cell_size = cell_size
        self.outline_width = outline_width
        self.width = grid.width * cell_size
        self.height = grid.height * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.agents_handler = AgentsHandler(agents)
        self.start = False

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
        for agent in self.agents:
            row = agent.row
            col = agent.col
            rect_x = col * self.cell_size
            rect_y = row * self.cell_size
            color = (255, 0, 0)
            pygame.draw.rect(
                self.screen, color,
                (rect_x, rect_y, self.cell_size, self.cell_size),
                0
            )

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == self.update_agents_event and self.start:
                    self.agents_handler.update_agents()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.start = True

            self.draw_grid()
            self.draw_agents()
            pygame.display.flip()

            ShowSim.clock.tick(60)


pygame.quit()


# Example usage:
if __name__ == "__main__":
    # Create a sample grid
    grid = make_maze_recursion(60, 60)

    pattern = []
    directions = (-1, 1)
    x, y = 0, 0
    pattern = []
    for i in range(10):
        pattern.append((0, i))

    for i in range(10):
        pattern.append((i, 9))

    for i in range(9, -1, -1):
        pattern.append((9, i))

    for i in range(9, -1, -1):
        pattern.append((i, 0))

    agent = Agent(1, 1)

    pattern = agent.astar(grid)
    agent.route_planned = pattern
    print("pattern: ", pattern)

    # Create and run the ShowGrid
    show_grid = ShowSim(grid, [agent])
    show_grid.run()

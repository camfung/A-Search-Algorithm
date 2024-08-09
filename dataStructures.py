from enum import Enum
import random
from typing import List


class Spot:
    def __init__(self, row, col, is_wall=False):
        self.row = row
        self.col = col
        self.is_wall = is_wall
        self.has_agent = False

    def set_wall(self):
        self.is_wall = True

    def __repr__(self):
        if self.has_agent:
            return "{A}"
        return "{x}" if self.is_wall else "{ }"


class Grid:
    def __init__(self, width, height, border_walls=False):
        self.width = width
        self.height = height
        self.grid = [[Spot(row, col) for col in range(width)]
                     for row in range(height)]
        self.border_walls = border_walls

        self.make_border_walls() if border_walls else None

    def make_border_walls(self):
        # Set the top and bottom rows as walls
        for col in range(self.width):
            self.grid[0][col].set_wall()
            self.grid[self.height - 1][col].set_wall()

        # Set the left and right columns as walls
        for row in range(self.height):
            self.grid[row][0].set_wall()
            self.grid[row][self.width - 1].set_wall()

    def drawStraightLine(self, startrow, startcol, direction):
        """
        Draws a straight line on the grid. The line must be either horizontal or vertical.
        """
        if direction == Direction.HORIZONTAL:
            for col in range(self.width):
                self.grid[startrow][col].set_wall()
        if direction == Direction.VERTICAL:
            for row in range(self.height):
                self.grid[row][startcol].set_wall()

    def __getitem__(self, index):
        return self.grid[index]

    def __repr__(self):
        return "\n".join(" ".join(str(spot) for spot in row) for row in self.grid)


class Direction(Enum):
    VERTICAL = 1
    HORIZONTAL = 2


class AStarSpot(Spot):
    def __init__(self, row: int = None, col: int = None, is_wall: bool = False, spot: Spot = None):
        if spot is not None:
            super().__init__(spot.row, spot.col, spot.is_wall)
        else:
            super().__init__(row, col, is_wall)
        self.g, self.h, self.f = 0, 0, 0


class AStarGrid(Grid):
    def __init__(self, width: int = None, height: int = None, border_walls: bool = True, grid: Grid = None):
        if grid is not None:
            if width is not None or height is not None:
                raise Exception(
                    "Cannot pass width or height  with a grid")
            super().__init__(grid.width, grid.height, grid.border_walls)
            self.grid = [[AStarSpot(spot=spot) for spot in col]
                         for col in grid.grid]
            print(self.grid)


class Agent:
    def __init__(self, row, col, route_planned=[]) -> None:
        self.row, self.col = row, col
        self.route_planned = route_planned
        self.route_travelled = []

    def step(self):
        if len(self.route_planned) < 1:
            raise Exception("reached the end of the path")
        row, col = self.route_planned.pop(0)
        self.row, self.col = row, col
        self.route_travelled.append((row, col))

    def __str__(self):
        return (
            f"Agent at position ({self.row}, {self.col})\n"
            f"Planned Route: {self.route_planned}\n"
            f"Traveled Route: {self.route_travelled}"
        )


class AgentsHandler:
    def __init__(self, agents) -> None:
        self.agents: List[Agent] = agents

    def update_agents(self):
        for agent in self.agents:
            try:
                agent.step()
            except Exception as e:
                agent.route_planned = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 9), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (
                    9, 9), (9, 9), (9, 8), (9, 7), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (9, 0), (9, 0), (8, 0), (7, 0), (6, 0), (5, 0), (4, 0), (3, 0), (2, 0), (1, 0), (0, 0)]

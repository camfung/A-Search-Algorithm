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
        return f"{{{self.row} , {self.col}}}" if self.is_wall else "{ }"


class Grid:
    def __init__(self, width, height, border_walls=False, fill=False):
        self.width = width
        self.height = height
        self.grid = [[Spot(row, col) for col in range(width)]
                     for row in range(height)]
        self.border_walls = border_walls

        self.make_border_walls() if border_walls else None
        if fill:
            self.fill_grid()

    def make_border_walls(self):
        # Set the top and bottom rows as walls
        for col in range(self.width):
            self.grid[0][col].set_wall()
            self.grid[self.height - 1][col].set_wall()

        # Set the left and right columns as walls
        for row in range(self.height):
            self.grid[row][0].set_wall()
            self.grid[row][self.width - 1].set_wall()

    def fill_grid(self):
        for col in self.grid:
            for spot in col:
                spot.is_wall = True

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
        self.g, self.h, self.f = 0, 0, 100000000
        self.neighbors = []
        self.previous = None

    def get_neighbors(self, grid):
        self.neighbors = []
        directions = [
            (0, -1),
            (0, 1),
            (-1, 0),
            (1, 0)
        ]

        for direction in directions:
            neighbor_row = self.row + direction[0]
            neighbor_col = self.col + direction[1]

            if 0 <= neighbor_row < grid.height and 0 <= neighbor_col < grid.width:
                neighbor = grid[neighbor_row][neighbor_col]
                if not neighbor.is_wall:
                    self.neighbors.append(neighbor)


class AStarGrid(Grid):
    def __init__(self, width: int = None, height: int = None, border_walls: bool = True, grid: Grid = None):
        if grid is not None:
            if width is not None or height is not None:
                raise Exception(
                    "Cannot pass width or height  with a grid")
            super().__init__(grid.width, grid.height, grid.border_walls)
            self.grid = [[AStarSpot(spot=spot) for spot in col]
                         for col in grid.grid]
            for col in self.grid:
                for spot in col:
                    spot.get_neighbors(self)


class Agent:
    def __init__(self, row, col, dest_row=0, dest_col=0, route_planned=[]) -> None:
        self.row, self.col = row, col
        self.route_planned = route_planned
        self.route_travelled = []
        self.destination = (dest_row, dest_col)
        self.color = (255, 0, 0)

    @property
    def desination(self):
        return self.destination

    @property
    def desination_row(self):
        return self.destination[0]

    @property
    def desination_col(self):
        return self.destination[1]

    def step(self, grid=None):
        if grid is not None:
            if self.route_planned[len(self.route_planned-1)] != self.desination:
                self.compute_planned_route(grid)
            else:
                # idk if i want this here or not yet
                raise Exception("passed grid to step without new destinaiton")

        if len(self.route_planned) < 1:
            raise Exception("reached the end of the path")
        row, col = self.route_planned.pop(0)
        self.row, self.col = row, col
        self.route_travelled.append((row, col))

    def get_h(self, s, e):
        return abs(e.col - s.col) + abs(e.row - s.row)

    def astar(self, grid: Grid):
        a_grid = AStarGrid(grid=grid)
        end = a_grid.grid[self.desination_row][self.desination_col]
        start = a_grid.grid[self.row][self.col]
        o_set = [start]
        c_set = []
        while o_set:
            lowest = o_set[0]
            for i in o_set:
                if i.f < lowest.f:
                    lowest = i

            current = lowest
            if current == end:
                path = []
                while current.previous is not None:
                    path.append((current.row, current.col))
                    current = current.previous
                path.append((current.row, current.col))
                path.reverse()
                return path

            o_set.remove(current)
            c_set.append(current)

            neighbors = current.neighbors
            for neighbor in neighbors:
                if neighbor not in c_set and not neighbor.is_wall:
                    tempg = current.g + 1
                    if tempg < neighbor.g:
                        neighbor.g = tempg
                        neighbor.previous = current
                    neighbor.h = self.get_h(neighbor, end)
                    neighbor.f = neighbor.g + neighbor.h
                    if neighbor not in o_set:
                        o_set.append(neighbor)
                        neighbor.previous = current
        raise NoRouteFoundError()

    def compute_planned_route(self, grid):
        self.route_planned = self.astar(grid)

    def __str__(self):
        return (
            f"Agent at position ({self.row}, {self.col})\n"
            f"Planned Route: {self.route_planned}\n"
            f"Traveled Route: {self.route_travelled}"
        )


class AgentsHandler:
    def __init__(self, agents: List[Agent], grid: Grid) -> None:
        self.agents: List[Agent] = agents
        self.grid: Grid = grid

    def update_agents(self):
        for agent in self.agents:
            try:
                agent.step()
            except Exception as e:
                pass
                # print("agent reached the end")
                # agent.route_planned = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 9), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (
                #     9, 9), (9, 9), (9, 8), (9, 7), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (9, 0), (9, 0), (8, 0), (7, 0), (6, 0), (5, 0), (4, 0), (3, 0), (2, 0), (1, 0), (0, 0)]

    def calculate_agents_routes(self):
        for agent in self.agents:
            agent.compute_planned_route(self.grid)


class NoRouteFoundError(Exception):
    def __init__(self, message="no Route Found") -> None:
        self.message = message
        super().__init__(message)

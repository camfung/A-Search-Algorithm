import datetime
import copy
from enum import Enum
from typing import List


class Spot:
    def __init__(self, row, col, is_wall=False):
        self.row = row
        self.col = col
        self.is_wall = is_wall
        self.has_agent = False

    @property
    def position(self):
        return (self.row, self.col)

    def set_wall(self):
        self.is_wall = True

    def __repr__(self):
        return f"{{{self.row}, {self.col}}}"


class Grid:
    def __init__(
        self, width=1, height=1, border_walls=False, fill=False, file_path=None
    ):
        self.width = width
        self.height = height
        if file_path:
            self.import_grid_from_file(file_path)
        else:
            self.grid = [
                [Spot(row, col) for col in range(width)] for row in range(height)
            ]
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

    def get_walls(self):
        walls = []
        for col in self.grid:
            for spot in col:
                if spot.is_wall:
                    walls.append((spot.row, spot.col))
        return walls

    def export(self):
        walls = self.get_walls()

        with open(str(datetime.datetime.now()), "w") as file:
            file.write(f"{self.width}, {self.height}\n")
            file.write(str(walls))

    def read_file_into_memory(self, filename):
        with open(filename, "r") as file:
            # Read the first line and convert it into a tuple of integers
            grid_size = tuple(map(int, file.readline().strip().split(",")))

            # Read the remaining lines and evaluate the string as a list of tuples
            coordinates = eval(file.readline().strip())

        return grid_size, tuple(coordinates)

    def import_grid_from_file(self, file_path: str):
        grid_size, walls = self.read_file_into_memory(file_path)
        self.import_grid(grid_size, walls)

    def import_grid(self, grid_size, walls):
        walls_dict = {coord: True for coord in walls}

        self.grid = []

        for row in range(grid_size[1]):
            grid_row = []
            for col in range(grid_size[0]):
                is_wall = walls_dict.get((row, col), False)
                spot = Spot(row, col, is_wall=is_wall)
                grid_row.append(spot)
            self.grid.append(grid_row)
        self.width = grid_size[0]
        self.height = grid_size[1]

    def __getitem__(self, index):
        return self.grid[index]

    def __repr__(self):
        return "\n".join(" ".join(str(spot) for spot in row) for row in self.grid)


class Direction(Enum):
    VERTICAL = 1
    HORIZONTAL = 2


class AStarSpot(Spot):
    def __init__(
        self,
        row: int = None,
        col: int = None,
        is_wall: bool = False,
        spot: Spot = None,
        previous=None,
    ):
        if spot is not None:
            super().__init__(spot.row, spot.col, spot.is_wall)
        else:
            super().__init__(row, col, is_wall)
        self.g, self.h, self.f = 100000000, 0, 100000000
        self.neighbors = []
        self.previous = previous

    def get_neighbors(self, grid):
        self.neighbors = []
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        for direction in directions:
            neighbor_row = self.row + direction[0]
            neighbor_col = self.col + direction[1]

            if 0 <= neighbor_row < grid.height and 0 <= neighbor_col < grid.width:
                neighbor = grid[neighbor_row][neighbor_col]
                if not neighbor.is_wall:
                    self.neighbors.append(neighbor)


class AStarGrid(Grid):
    def __init__(
        self,
        width: int = None,
        height: int = None,
        border_walls: bool = True,
        grid: Grid = None,
    ):
        if grid is not None:
            if width is not None or height is not None:
                raise Exception("Cannot pass width or height  with a grid")
            super().__init__(grid.width, grid.height, grid.border_walls)
            self.grid = [[AStarSpot(spot=spot) for spot in col] for col in grid.grid]
            for col in self.grid:
                for spot in col:
                    spot.get_neighbors(self)


class Agent:
    _id_counter = 0

    def __init__(self, row, col, dest_row=0, dest_col=0, route_planned=[]) -> None:
        self.row, self.col = row, col
        self.route_planned = route_planned
        self.route_travelled = []
        self._destination = (dest_row, dest_col)
        self.color = (255, 0, 0)
        self.id = Agent._id_counter
        Agent._id_counter += 1

    @property
    def pos(self):
        return (self.row, self.col)

    @pos.setter
    def pos(self, value):
        self.row = value[0]
        self.col = value[1]

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, value):
        self._destination = value

    @property
    def desination_row(self):
        return self.destination[0]

    @property
    def desination_col(self):
        return self.destination[1]

    def step(self, grid=None, new_desination=None):
        if grid is not None:
            if self.route_planned[len(self.route_planned) - 1] != self.destination:
                self.compute_planned_route(grid)
            elif new_desination is not None:
                self.destination = new_desination
                self.compute_planned_route(grid=grid)

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
        start.g = 0
        o_set = [start]
        c_set = []
        while o_set:
            lowest = o_set[0]
            for spot in o_set:
                if spot.f < lowest.f:
                    lowest = spot
                elif spot.f == lowest.f and spot.h < lowest.h:
                    lowest = spot

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
        for _, agent in enumerate(self.agents):
            try:
                agent.step(self.grid)
            except Exception as e:
                print(e)

    def calculate_agents_routes(self):
        for agent in self.agents:
            agent.compute_planned_route(self.grid)

    def add_agent(self, agent: Agent):
        agent.compute_planned_route(self.grid)
        self.agents.append(agent)

    def update_agent_dest(self, agent_id, pos):
        self.agents[agent_id].row = pos[0]
        self.agents[agent_id].col = pos[1]


class NoRouteFoundError(Exception):
    def __init__(self, message="no Route Found") -> None:
        self.message = message
        super().__init__(message)


class LoopingAgent(Agent):
    def __init__(self, row, col, dest_row=0, dest_col=0, route_planned=[]) -> None:
        super().__init__(row, col, dest_row, dest_col, route_planned)

    def step(self, grid=None, new_desination=None):
        try:
            if grid is not None:
                if self.route_planned[len(self.route_planned) - 1] != self.destination:
                    self.compute_planned_route(grid)
                elif new_desination is not None:
                    self.destination = new_desination
                    self.compute_planned_route(grid=grid)
        except Exception:
            pass

        if len(self.route_planned) < 1:
            self.destination = self.route_travelled[0]
            self.route_travelled.reverse()
            self.route_planned = [copy.deepcopy(cord) for cord in self.route_travelled]
            self.route_travelled.clear()

        if self.route_planned:
            row, col = self.route_planned.pop(0)
            self.row, self.col = row, col
            self.route_travelled.append((row, col))

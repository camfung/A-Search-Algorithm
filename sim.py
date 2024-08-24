from dataStructures import Grid, Agent, AgentsHandler
from MakeMaze import make_maze_recursion


class Direction:
    HORIZONTAL = 1
    VERTICAL = 2


class Sim:
    def __init__(
        self,
        grid: Grid,
        agents_handler: AgentsHandler,
        outline_width=1,
    ):
        self.grid = grid
        self.outline_width = outline_width
        self.agents_handler = agents_handler
        self.start = False
        self.last_tile_flipped = (-1, -1)
        self.brush_radius = 0

    def set_is_wall(self, pos):
        center_row = pos[0]
        center_col = pos[1]

        if self.brush_radius < 1:
            grid[center_row][center_col].is_wall = True
            return
        start = (center_row - self.brush_radius, center_col - self.brush_radius)
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
        if self.brush_radius < 1:
            grid[center_row][center_col].is_wall = False
            return
        start = (center_row - self.brush_radius, center_col - self.brush_radius)
        end = (center_row + self.brush_radius, center_col + self.brush_radius)
        for row in range(start[0], end[0]):
            for col in range(start[1], end[1]):
                grid[row][col].is_wall = False

    def run(self):
        running = True
        while running:
            self.agents_handler.update_agents()

    def set_agent_dest(self, agent_id: int = -1, pos=(-1, -1)):
        if agent_id < 0:
            raise ValueError("invalid Agent_id")

        elif pos[0] < 0 or pos[1] < 0:
            raise ValueError("invalid position")
        elif pos[0] < 0 or pos[0] > self.grid.height:
            raise ValueError("invalid position")
        elif pos[0] < 0 or pos[0] > self.grid.height:
            raise ValueError("invalid position")
        elif pos[1] < 0 or pos[1] > self.grid.width:
            raise ValueError("invalid position")
        elif pos[1] < 0 or pos[1] > self.grid.width:
            raise ValueError("invalid position")

        self.agents_handler.update_agent_dest(agent_id, pos)


if __name__ == "__main__":
    grid_width, grid_height = 100, 100
    # 340, 130
    grid = make_maze_recursion(grid_width, grid_height)
    # grid = Grid(width=grid_width, height=grid_height,
    #             border_walls=True, fill=True)
    # grid = Grid(file_path="./test.txt")

    agents = [
        Agent(1, 1, grid_height - 2, grid_width - 2),
        # Agent(1, grid_width-2, grid_height-2, 1),
        # Agent(grid_height-2, 1, 1, grid_width-2),
        # Agent(grid_height-2, grid_width-2, 1, 1)
    ]

    agents_handler = AgentsHandler(agents=agents, grid=grid)

    show_grid = Sim(grid, agents_handler)
    show_grid.run()

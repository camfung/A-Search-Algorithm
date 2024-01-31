import pygame as pg
import sys
import random
from math import hypot
import time
from dividealgo import Spot
from dividealgo import Grid
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR
from config import SPOT_SIZE, GRID_WIDTH, GRID_HEIGHT
from config import PASSAGE_WIDTH, DEBUG, SHOW_OUTLINES, MAKE_BOARDER_WALLS
from config import SpotState
from config import EMPTY_COLOR, WALL_COLOR, PATH_COLOR, END_COLOR, START_COLOR
# using the euclidian distance


def get_h(s, e):
    return abs(e.x_cord - s.x_cord) + abs(e.y_cord - s.y_cord)


# def get_grid_x():
#     return int(pygame.mouse.get_pos()[0] / (pixels / side_length))


# def get_grid_y():
#     return int(pygame.mouse.get_pos()[1] / (pixels / side_length))


class AdvancedSpot(Spot):
    def __init__(self, row=0, col=0, g=1000000, h=0, f=0, is_start=False, is_end=False, existing_spot=None):
        if existing_spot:
            self.row = existing_spot.row
            self.col = existing_spot.col
            self.state = existing_spot.state
            self.x = existing_spot.x
            self.y = existing_spot.y
        else:
            super().__init__(row, col)
            self.state = SpotState.EMPTY
        self._g = g
        self._h = h
        self._f = f
        self.neighbors = []
        self.previous = None

    def draw(self, screen):
        color = self.getColor()
        outline_thickness = 1
        outline_color = (0, 0, 0)
        if self.state and not SHOW_OUTLINES:
            pg.draw.rect(screen, color, (self.x, self.y, SPOT_SIZE, SPOT_SIZE))

        outline_thickness = 1  # Thickness of the outline
        if SHOW_OUTLINES:
            # Draw the outline rectangle
            pg.draw.rect(screen, outline_color, (self.x - outline_thickness, self.y - outline_thickness,
                                                 SPOT_SIZE + 2 * outline_thickness, SPOT_SIZE + 2 * outline_thickness))

            # Draw the inner rectangle
            pg.draw.rect(screen, color, (self.x, self.y, SPOT_SIZE, SPOT_SIZE))

    def get_euclidian_distance(self, target):
        return abs(target.col - self.col) + abs(target.row - self.row)

    def getColor(self):
        if self.state == SpotState.EMPTY:
            return EMPTY_COLOR
        elif self.state == SpotState.WALL:
            return WALL_COLOR
        elif self.state == SpotState.PATH:
            return PATH_COLOR
        elif self.state == SpotState.END:
            return END_COLOR
        elif self.state == SpotState.START:
            return START_COLOR
    # G setter and getter

    @property
    def g(self):
        return self._g

    @g.setter
    def g(self, value):
        self._g = value

    # H setter (as Euclidean distance) and getter
    @property
    def h(self):
        return self._h

    @h.setter
    def h(self, target):
        self._h = self.get_euclidian_distance(target)

    # F setter and getter
    @property
    def f(self):
        return self._f

    @f.setter
    def f(self, value):
        self._f = value


class AStarGrid(Grid):
    def __init__(self, width=None, height=None, start=None, end=None, existing_grid=None, spot_class=AdvancedSpot):
        # Check if an existing grid is provided
        if existing_grid is not None:
            # Set up the AStarGrid based on the existing grid
            self.width = existing_grid.width
            self.height = existing_grid.height
            self.grid = [[spot_class(existing_spot=existing_grid.grid[row][col]) for col in range(self.width)]
                         for row in range(self.height)]

        else:
            # Ensure width and height are provided for a new grid
            if width is None or height is None:
                raise ValueError(
                    "Width and height must be provided for a new grid")

            # Call the super constructor with the custom spot_class
            super().__init__(width, height, spot_class=spot_class)

        # Common setup for both new and existing grids
        if not start:
            start = (0, 0)
        if not end:
            end = (self.width - 1, self.height - 1)

        self.o_set = []  # Open set for A* algorithm
        self.c_set = []  # Closed set for A* algorithm
        self.start = start  # Starting position (row, col)
        self.end = end  # Ending position (row, col)
        self.path = []
        self.set_neighbors()
        self.get_start().state = SpotState.START
        self.get_end().state = SpotState.END

    def get_start(self):
        return self.grid[self.start[0]][self.start[1]]

    def get_end(self):
        return self.grid[self.end[0]][self.end[1]]

    def set_neighbors(self):
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                # Clear the neighbors list for each node before adding neighbors
                self.grid[j][i].neighbors = []

                # Check for neighbor above
                if i > 0:
                    self.grid[j][i].neighbors.append(self.grid[j][i-1])

                # Check for neighbor below
                if i < GRID_HEIGHT - 1:
                    self.grid[j][i].neighbors.append(self.grid[j][i+1])

                # Check for neighbor to the left
                if j > 0:
                    self.grid[j][i].neighbors.append(self.grid[j-1][i])

                # Check for neighbor to the right
                if j < GRID_WIDTH - 1:
                    self.grid[j][i].neighbors.append(self.grid[j+1][i])

    def find_lowest_f_spot(self):
        if not self.o_set:
            raise ValueError("Open set is empty")

        lowest = self.o_set[0]
        for spot in self.o_set:
            if spot.f < lowest.f:
                lowest = spot

        if lowest == self.end:
            print("done")
            return lowest
        else:
            return lowest

    def a_star(self):
        self.o_set.append(self.get_start())
        while self.o_set:
            current = self.find_lowest_f_spot()

            self.o_set.remove(current)
            self.c_set.append(current)

            # checking the neighbors of the current
            neighbors = current.neighbors
            for neighbor in neighbors:
                if neighbor not in self.c_set and neighbor.state is not SpotState.WALL:
                    temp_g = current.g + 1
                    if temp_g < neighbor.g:
                        neighbor.g = temp_g
                        neighbor.previous = current
                    neighbor.h = self.get_end()
                    neighbor.f = neighbor.g + neighbor.h
                    if neighbor not in self.o_set:
                        self.o_set.append(neighbor)
                        neighbor.previous = current
        dist = 0
        path = []
        temp = self.get_end()  # Assuming `current` is the last spot reached
        while temp.previous:
            dist += 1
            temp.previous.state = SpotState.PATH
            path.append(temp.previous)
            temp = temp.previous
        self.path.append(self.get_end())
        self.path = path
# dropping piece
# if pygame.mouse.get_pressed(3)[0]:
#     pygame.draw.rect(wn, (0, 0, 0), pygame.Rect(get_grid_x() * spot_size + 1,
#                                                 get_grid_y() * spot_size + 1, spot_size - 2, spot_size - 2))
#     grid[get_grid_y()][get_grid_x()].is_wall = True
# if event.type == pygame.constants.MOUSEBUTTONDOWN:
#     if event.button == 3:
#         print(grid[get_grid_y()][get_grid_x()].f)

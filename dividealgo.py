# Import Pygame
import random
import pygame as pg
from enum import Enum

from config import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR
from config import SPOT_SIZE, GRID_WIDTH, GRID_HEIGHT
from config import PASSAGE_WIDTH, DEBUG, SHOW_OUTLINES, MAKE_BOARDER_WALLS
from config import SpotState


def divide(grid, startx=None, endx=None, starty=None, endy=None, orientation="vertical"):

    if startx is None:
        startx = 0
    if endx is None:
        endx = grid.width - 1  # Assuming grid has a 'width' attribute
    if starty is None:
        starty = 0
    if endy is None:
        endy = grid.height - 1  # Assuming grid has a 'height' attribute

    if orientation == "horizontal" and endy - starty <= PASSAGE_WIDTH:
        return
    elif orientation == "vertical" and endx - startx <= PASSAGE_WIDTH:
        return

    if orientation == "horizontal":
        middle = starty + (endy - starty) // 2
        grid.splitGrid(middle, startx, middle, endx)
        divide(grid, startx, endx, starty, middle, "vertical")
        divide(grid, startx, endx, middle+1, endy, "vertical")

    elif orientation == "vertical":
        middle = startx + (endx - startx) // 2
        grid.splitGrid(starty, middle, endy, middle)

        divide(grid, startx, middle, starty, endy, "horizontal")
        divide(grid, middle+1, endx, starty, endy, "horizontal")


class Spot:
    def __init__(self, row=0, col=0, state=SpotState.EMPTY):

        self.row = row
        self.col = col
        self.state = state
        self.x = col * SPOT_SIZE
        self.y = row * SPOT_SIZE

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

    def __str__(self):
        return f"row: {self.row}, col: {self.col}, state: {self.state}"

    def getColor(self):
        if self.state == SpotState.EMPTY:
            return (255, 255, 255)
        elif self.state == SpotState.WALL:
            return (0, 0, 0)

    def set_wall(self):
        self.state = SpotState.WALL

    def __repr__(self):
        return "{x}" if self.state == SpotState.WALL else "{ }"


class Grid:
    def __init__(self, width, height, spot_class=Spot):
        self.width = width
        self.height = height
        self.grid = [[spot_class(row, col) for col in range(width)]
                     for row in range(height)]

    def draw(self, screen):
        for row in range(self.height):
            for col in range(self.width):
                self.grid[row][col].draw(screen)

    def make_border_walls(self):
        # Set the top and bottom rows as walls
        for col in range(self.width):
            self.grid[0][col].set_wall()
            self.grid[self.height - 1][col].set_wall()

        # Set the left and right columns as walls
        for row in range(self.height):
            self.grid[row][0].set_wall()
            self.grid[row][self.width - 1].set_wall()

    def drawStraightLine(self, startrow, startcol, endrow, endcol):
        """
        Draws a straight line on the grid. The line must be either horizontal or vertical.
        """
        # choose a random index to not make a wall
        if startrow == endrow:  # Horizontal line
            middle = startcol + (endcol - startcol) // 2
            for col in range(startcol, endcol + 1):
                self.grid[startrow][col].set_wall()
        elif startcol == endcol:  # Vertical line
            for row in range(startrow, endrow + 1):
                self.grid[row][startcol].set_wall()

    def splitGrid(self, startrow, startcol, endrow, endcol):
        """
        Draws a straight line on the grid. The line must be either horizontal or vertical.
        """
        # choose a random index to not make a wall
        if startrow == endrow:  # Horizontal line
            middle = startrow + (endrow - startrow) // 2
            random_index = 0
            while True:
                random_index = startcol + 1
                # random_index = random.randint(startrow, endrow)
                if random_index != middle:
                    break

            for col in range(startcol, endcol + 1):
                if col == random_index:
                    continue
                self.grid[startrow][col].set_wall()
        elif startcol == endcol:  # Vertical line
            middle = startcol + (endcol - startcol) // 2
            random_index = 0
            while True:
                random_index = startcol+1
                # random_index = random.randint(startrow, endrow)
                if random_index != middle:
                    break

            for row in range(startrow, endrow + 1):
                if row == random_index:
                    continue
                if random_index != middle:
                    break

            for col in range(startcol, endcol + 1):
                if col == random_index:
                    continue
                self.grid[startrow][col].set_wall()
        elif startcol == endcol:  # Vertical line
            middle = startcol + (endcol - startcol) // 2
            random_index = 0
            while True:
                random_index = random.randint(startrow, endrow)
                if random_index != middle:
                    break

            for row in range(startrow, endrow + 1):
                if row == random_index:
                    continue
                self.grid[row][startcol].set_wall()

    def __repr__(self):
        return "\n".join(" ".join(str(spot) for spot in row) for row in self.grid)

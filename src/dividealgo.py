# Import Pygame
from enum import Enum
import random
import pygame as pg


# Constants for screen dimensions
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 1300
BACKGROUND_COLOR = (3, 12, 23)  # White color
# GRID_WIDTH = 100
# GRID_HEIGHT = 100
# SPOT_SIZE = SCREEN_HEIGHT // GRID_HEIGHT  # Size of each spot in pixels

SPOT_SIZE = 100
GRID_WIDTH = SCREEN_WIDTH // SPOT_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // SPOT_SIZE
PASSAGE_WIDTH = 5
DEBUG = False
SHOW_OUTLINES = True
MAKE_BOARDER_WALLS = True


def divide(grid, startx, endx, starty, endy, orientation="vertical"):

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


def pygame_loop(grid):
    if not DEBUG:
        pg.init()

        # Set up the screen with configurable dimensions
        screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption('Pygame Project')

        running = True
        while running:
            # Fill the screen with the background color
            screen.fill(BACKGROUND_COLOR)

            # Event loop
            for event in pg.event.get():
                # Check for QUIT event to exit the loop
                if event.type == pg.QUIT:
                    running = False
            grid.draw(screen)
            # Update the display
            pg.display.flip()

        # Quit Pygame
        pg.quit()


def get_h(s, e):
    return abs(e.x_cord - s.x_cord) + abs(e.y_cord - s.y_cord)


def a_star(grid):
    end = grid.grid[grid.height-1][grid.height-1]
    start = grid.grid[0][0]
    o_set = [start]
    c_set = []
    dist = 0
    while o_set:
        lowest = o_set[0]
        for i in o_set:
            if i.f < lowest.f:
                lowest = i

        current = lowest
        if current == end:
            path = []
            while current.previous is not None:
                path.append(current)
                current = current.previous
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
                neighbor.h = get_h(neighbor, end)
                neighbor.f = neighbor.g + neighbor.h
                if neighbor not in o_set:
                    o_set.append(neighbor)
                    neighbor.previous = current


def main():
    grid = Grid(GRID_WIDTH, GRID_HEIGHT)
    grid.drawStraightLine(10, 10, Direction.VERTICAL)
    print(grid)
    print(a_star(grid))


if __name__ == '__main__':
    main()

import datetime
from config import *
import pygame as pg
from dividealgo import Grid, divide
from astar import AStarGrid


def main():
    now = datetime.datetime.now()
    grid = Grid(GRID_WIDTH, GRID_HEIGHT)
    divide(grid)
    grid = AStarGrid(existing_grid=grid)
    if MAKE_BOARDER_WALLS:
        grid.make_border_walls()
    grid.a_star()
    end = datetime.datetime.now()

    print(end-now)
    if DEBUG:
        for spot in grid.path:
            print(spot)

    # Main game loop
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


if __name__ == '__main__':
    main()

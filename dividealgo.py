# Import Pygame
import random
import pygame as pg


# Constants for screen dimensions
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 1300
BACKGROUND_COLOR = (3, 12, 23)  # White color
# GRID_WIDTH = 100
# GRID_HEIGHT = 100
# SPOT_SIZE = SCREEN_HEIGHT // GRID_HEIGHT  # Size of each spot in pixels

SPOT_SIZE = 110
GRID_WIDTH = SCREEN_WIDTH // SPOT_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // SPOT_SIZE
PASSAGE_WIDTH = 2
DEBUG = False
SHOW_OUTLINES = True
MAKE_BOARDER_WALLS = True

# divide(grid, startx, endx, starty, endy, orientation):
#     if endx - startx <= 1 or endy - starty <= 1:
#         return
#     if orientation == "horizontal":
#         use y
#         middle = (endy - starty) / 2
#         // draw line down middle
#         // i'm not sure how to do this part.
#         divide(grid, startx, endx, starty, middle -1, "vertical")
#         divide(grid, startx, endx, middle, endy, "vertical")

#     else if orientiation == "vertical"
#         use x
#         middle = (endx - startx) / 2
#         // draw line down middle
#         // i'm not sure how to do this part.
#         divide(grid, startx, middle-1, starty, endy, "horizontal")
#         divide(grid, middle, endx, starty, endy, "horizontal")


def divide(grid, startx, endx, starty, endy, orientation="vertical"):

    if orientation == "horizontal" and endy - starty <= PASSAGE_WIDTH:
        return
    elif orientation == "vertical" and endx - startx <= PASSAGE_WIDTH:
        return

    if orientation == "horizontal":
        middle = starty + (endy - starty) // 2
        grid.drawStraightLine(middle, startx, middle, endx)
        divide(grid, startx, endx, starty, middle, "vertical")
        divide(grid, startx, endx, middle+1, endy, "vertical")

    elif orientation == "vertical":
        middle = startx + (endx - startx) // 2
        grid.drawStraightLine(starty, middle, endy, middle)

        divide(grid, startx, middle, starty, endy, "horizontal")
        divide(grid, middle+1, endx, starty, endy, "horizontal")
# Spot class


class Spot:
    def __init__(self, row, col, is_wall=False):
        self.row = row
        self.col = col
        self.is_wall = is_wall
        self.x = col * SPOT_SIZE
        self.y = row * SPOT_SIZE

    def draw(self, screen):
        color = (0, 0, 255) if self.is_wall else (255, 255, 255)
        outline_thickness = 1
        outline_color = (0, 0, 0)
        if self.is_wall and not SHOW_OUTLINES:
            pg.draw.rect(screen, color, (self.x, self.y, SPOT_SIZE, SPOT_SIZE))

        outline_thickness = 1  # Thickness of the outline
        if SHOW_OUTLINES:
            # Draw the outline rectangle
            pg.draw.rect(screen, outline_color, (self.x - outline_thickness, self.y - outline_thickness,
                                                 SPOT_SIZE + 2 * outline_thickness, SPOT_SIZE + 2 * outline_thickness))

            # Draw the inner rectangle
            pg.draw.rect(screen, color, (self.x, self.y, SPOT_SIZE, SPOT_SIZE))

    def set_wall(self):
        self.is_wall = True

    def __repr__(self):
        return "{x}" if self.is_wall else "{ }"


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[Spot(row, col) for col in range(width)]
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

    def __repr__(self):
        return "\n".join(" ".join(str(spot) for spot in row) for row in self.grid)


def main():
    grid = Grid(GRID_WIDTH, GRID_HEIGHT)
    if MAKE_BOARDER_WALLS:
        grid.make_border_walls()
    print(grid)
    divide(grid, 0, grid.width-1, 0, grid.height-1)
    print(grid)
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

# Import Pygame
import random
import pygame as pg

# Constants for screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
BACKGROUND_COLOR = (255, 255, 255)  # White color
SPOT_SIZE = 70  # Size of each spot in pixels

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
    if endx - startx <= 2 or endy - starty <= 2:
        yield
        return
    if orientation == "horizontal":
        middle = starty + (endy - starty) // 2
        grid.drawStraightLine(middle, startx, middle, endx)
        yield
        yield from divide(grid, startx, endx, starty, middle-1, "vertical")
        yield
        yield from divide(grid, startx, endx, middle+1, endy, "vertical")

    elif orientation == "vertical":
        middle = startx + (endx - startx) // 2
        grid.drawStraightLine(starty, middle, endy, middle)
        yield
        yield from divide(grid, startx, middle-1, starty, endy, "horizontal")
        yield
        yield from divide(grid, middle+1, endx, starty, endy, "horizontal")

# Spot class


class Spot:
    def __init__(self, row, col, is_wall=False):
        self.row = row
        self.col = col
        self.is_wall = is_wall
        self.x = row * SPOT_SIZE
        self.y = col * SPOT_SIZE

    def draw(self, screen):
        color = (0, 0, 255) if self.is_wall else (255, 255, 255)
        outline_thickness = 1
        outline_color = (0, 0, 0)
        # if self.is_wall:
        # pg.draw.rect(screen, color, (self.x, self.y, SPOT_SIZE, SPOT_SIZE))
        # pg.draw.rect(screen, (0, 0, 0), (self.x - outline_thickness, self.y -
        #                                  outline_thickness, SPOT_SIZE + 2 * outline_thickness, SPOT_SIZE + 2 * outline_thickness))

        outline_thickness = 1  # Thickness of the outline

        # Draw the outline rectangle
        pg.draw.rect(screen, outline_color, (self.x - outline_thickness, self.y - outline_thickness,
                     SPOT_SIZE + 2 * outline_thickness, SPOT_SIZE + 2 * outline_thickness))

        # Draw the inner rectangle
        pg.draw.rect(screen, color, (self.x, self.y, SPOT_SIZE, SPOT_SIZE))

    def set_wall(self):
        self.is_wall = True


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
        line must be horizontal or vertical
        """
        if startrow == endrow:
            for i in range(startcol, endcol+1):
                self.grid[i][startrow].set_wall()
        elif startcol == endcol:
            for i in range(startrow, endrow+1):
                self.grid[startcol][i].set_wall()


def main():
    # Initialize Pygame
    pg.init()

    # Set up the screen with configurable dimensions
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption('Pygame Project')

    grid = Grid(SCREEN_WIDTH // SPOT_SIZE, SCREEN_HEIGHT // SPOT_SIZE)
    grid.make_border_walls()

    # Create generator object
    divider = divide(grid, 0, grid.width-1, 0, grid.height-1)

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    # Advance the generator
                    try:
                        next(divider)
                    except StopIteration:
                        pass

        grid.draw(screen)
        pg.display.flip()


if __name__ == '__main__':
    main()

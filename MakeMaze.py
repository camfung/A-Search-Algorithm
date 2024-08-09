from dataStructures import Grid
import random


def make_maze_recursive_call(maze, top, bottom, left, right):
    """
    Recursive function to divide up the maze in four sections
    and create three gaps.
    Walls can only go on even numbered rows/columns.
    Gaps can only go on odd numbered rows/columns.
    Maze must have an ODD number of rows and columns.
    """
    # Figure out where to divide horizontally
    start_range = bottom + 2
    end_range = top - 1
    y = random.randrange(start_range, end_range, 2)

    # Do the division
    for column in range(left + 1, right):
        maze[y][column].is_wall = True

    # Figure out where to divide vertically
    start_range = left + 2
    end_range = right - 1
    x = random.randrange(start_range, end_range, 2)

    # Do the division
    for row in range(bottom + 1, top):
        maze[row][x].is_wall = True

    # Now we'll make a gap on 3 of the 4 walls.
    # Figure out which wall does NOT get a gap.
    wall = random.randrange(4)
    if wall != 0:
        gap = random.randrange(left + 1, x, 2)
        maze[y][gap].is_wall = False
    if wall != 1:
        gap = random.randrange(x + 1, right, 2)
        maze[y][gap].is_wall = False
    if wall != 2:
        gap = random.randrange(bottom + 1, y, 2)
        maze[gap][x].is_wall = False
    if wall != 3:
        gap = random.randrange(y + 1, top, 2)
        maze[gap][x].is_wall = False

    # If there's enough space, to a recursive call.
    if top > y + 3 and x > left + 3:
        make_maze_recursive_call(maze, top, y, left, x)
    if top > y + 3 and x + 3 < right:
        make_maze_recursive_call(maze, top, y, x, right)
    if bottom + 3 < y and x + 3 < right:
        make_maze_recursive_call(maze, y, bottom, x, right)
    if bottom + 3 < y and x > left + 3:
        make_maze_recursive_call(maze, y, bottom, left, x)


def make_maze_recursion(maze_width, maze_height):
    """ Make the maze by recursively splitting it into four rooms. """
    grid = Grid(maze_width, maze_height, border_walls=True)

    # Start the recursive process
    make_maze_recursive_call(grid, maze_height - 1, 0, 0, maze_width - 1)
    return grid

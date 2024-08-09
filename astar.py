import pygame
import sys
import random
from math import hypot
import time


def a_star(grid):
    end = grid[side_length-1][side_length-1]
    start = grid[0][0]
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

    temp = end
    dist = 0
    path = []
    while temp.previous:
        dist += 1
        path.append(temp.previous)
        temp = temp.previous

    for i in path:
        pygame.draw.rect(wn, (0, 0, 255), pygame.Rect(i.y_cord,
                                                      i.x_cord, 1, 1))

    # making the end square blue
    pygame.draw.rect(wn, (0, 0, 255), pygame.Rect(end.y_cord,
                                                  end.x_cord, 1, 1))

    time.sleep(0)
    print(dist)


# using the euclidian distance
def get_h(s, e):
    return abs(e.x_cord - s.x_cord) + abs(e.y_cord - s.y_cord)


def get_grid_x():
    return int(pygame.mouse.get_pos()[0] / (pixels / side_length))


def get_grid_y():
    return int(pygame.mouse.get_pos()[1] / (pixels / side_length))


class Spot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_cord = spot_size * x
        self.y_cord = spot_size * y
        self.g = 1000
        self.h = 0
        self.f = 0
        self.is_wall = False
        self.neighbors = []
        self.previous = None


pygame.init()
pixels = 1000
wn = pygame.display.set_mode((pixels, pixels))
wn.fill((255, 255, 255))

# array for the path that is being created
path = []

# setting up grid
side_length = 1000
spot_size = pixels / side_length
prob = 0

grid = []

# adding all the spots to the grid
for i in range(0, side_length):
    wall = False
    temp = []
    grid.append(temp)
    for j in range(0, side_length):
        grid[i].append(Spot(i, j))
        pygame.draw.rect(wn, (0, 0, 0),
                         pygame.Rect(grid[i][j].y_cord, grid[i][j].x_cord, spot_size, spot_size), 1)
        num = random.randint(0, prob)
        if num == 0 and i != side_length - 1 and j != side_length - 1:
            grid[i][j].is_wall = True

# getting the neighbors of each of the spots
for i in range(0, side_length):
    for j in range(0, side_length):
        if 0 < i <= side_length - 1:
            grid[j][i].neighbors.append(grid[j][i - 1])
        if 0 <= i < side_length - 1:
            grid[j][i].neighbors.append(grid[j][i + 1])
        if 0 <= j < side_length - 1:
            grid[j][i].neighbors.append(grid[j + 1][i])
        if 0 < j <= side_length - 1:
            grid[j][i].neighbors.append(grid[j - 1][i])


end = grid[side_length-1][side_length-1]
start = grid[0][0]
o_set = [start]
c_set = []

while True:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                a_star()

        # dropping piece
        if pygame.mouse.get_pressed(3)[0]:
            pygame.draw.rect(wn, (0, 0, 0), pygame.Rect(get_grid_x() * spot_size + 1,
                                                        get_grid_y() * spot_size + 1, spot_size - 2, spot_size - 2))
            grid[get_grid_y()][get_grid_x()].is_wall = True
        if event.type == pygame.constants.MOUSEBUTTONDOWN:
            if event.button == 3:
                print(grid[get_grid_y()][get_grid_x()].f)

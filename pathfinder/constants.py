"""Constants go here"""
import os

import pygame

light_gray = (175, 175, 175)
medium_gray = (140, 140, 140)
dark_gray = (110, 110, 110)
very_dark_gray = (50, 50, 50)

# Primary, black, white and other colors
# white = (255, 255, 255)
white = (230, 230, 230)
pink = (252, 15, 192)
dark_pink = (187, 0, 255)
red = (255, 0, 0)
dark_red = (215, 0, 0)
orange = (255, 140, 0)
yellow = (255, 254, 106)
green = (0, 255, 0)
blue = (64, 206, 227)
# blue = (0, 190, 218)
# blue = (175, 216, 248)
light_blue = (66, 236, 245)
black = (12, 53, 71)
# black = (0, 0, 0)

grid_x, grid_y = 50, 25
grid_offset = (grid_x - 1, grid_y - 1)
WIDTH, HEIGHT = 1400, 700
OFFSET = 3
ZERO = (0, 0)
XGR = (grid_x - 1, 0)
YGR = (0, grid_y - 1)
weighted = ('astar', 'dijkstra', 'greedy')
node_size = (25, 25)
spaceship = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'spaceship.png')), node_size)
search_speed = 0.0065
TOP_LEFT_X = HEIGHT // grid_y * 0 + OFFSET
TOP_LEFT_Y = HEIGHT // grid_y * 0 + OFFSET
SEARCH_COLORS = (dark_pink, blue, yellow)
TARGET_COLORS = [red, green, pink]
THE_GRID = {}
for x in range(grid_x):
    for y in range(grid_y):
        THE_GRID[(x, y)] = float("inf")

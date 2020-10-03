"""Constants go here"""
import os

import pygame

from settings import Settings

# load settings from settings.json
settings = Settings('settings.json')

# Version
version = settings.version

# Colors
WHITE = (230, 230, 230)
PINK = (252, 15, 192)
DARK_PINK = (187, 0, 255)
RED = (255, 0, 0)
ORANGE = (255, 140, 0)
YELLOW = (255, 254, 106)
GREEN = (0, 255, 0)
BLUE = (64, 206, 227)
DARK_BLUE = (15, 66, 88)

OFFSET = 3

WIDTH, HEIGHT = settings.screen_size["WIDTH"], settings.screen_size["HEIGHT"]
grid_x, grid_y = settings.grid_size["WIDTH"], settings.grid_size["HEIGHT"]
grid_size = grid_x, grid_y
grid_offset = (grid_x - 1, grid_y - 1)

weight_density = settings.weight_density
default_alg = settings.default_alg
XGR = (grid_x - 1, 0)
YGR = (0, grid_y - 1)

node_size = settings.node_size
spaceship = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'spaceship.png')), node_size)

SEARCH_COLORS = (DARK_PINK, BLUE, YELLOW)
TARGET_COLORS = [RED, GREEN, PINK]
THE_GRID = {(x, y): float("inf") for y in range(grid_y) for x in range(grid_x)}

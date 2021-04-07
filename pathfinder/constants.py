"""Constants go here"""
import os
from collections import namedtuple

import pygame

from settings import Settings

# load settings from settings.json
settings = Settings('settings.json')

# Version
version = settings.version

Color = namedtuple('Color', ['r', 'g', 'b'])

# Colors
if settings.dark_mode:
    WHITE = DARK_MODE_WHITE = Color(100, 100, 100)
else:
    WHITE = LIGHT_MODE_WHITE = Color(255, 255, 255)

PINK = Color(252, 15, 192)
DARK_PINK = Color(187, 0, 255)
RED = Color(255, 0, 0)
ORANGE = Color(255, 140, 0)
YELLOW = Color(255, 254, 106)
GREEN = Color(0, 255, 0)
BLUE = Color(64, 206, 227)
DARK_BLUE = Color(15, 66, 88)

OFFSET = 3

WIDTH, HEIGHT = settings.screen_size["WIDTH"], settings.screen_size["HEIGHT"]
GRID_X, GRID_Y = settings.grid_size["WIDTH"], settings.grid_size["HEIGHT"]
GRID_SIZE: tuple = GRID_X, GRID_Y
GRID_OFFSET: tuple = (GRID_X - 1, GRID_Y - 1)

weight_density: int = settings.weight_density
default_alg = settings.default_alg
XGR = (GRID_X - 1, 0)
YGR = (0, GRID_Y - 1)

node_size = settings.node_size

stretch_factor = (node_size, node_size)
SPACESHIP = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'spaceship.png')), stretch_factor)

SEARCH_COLORS = (DARK_PINK, BLUE, YELLOW)
TARGET_COLORS = [RED, GREEN, PINK]
THE_GRID = {(x, y): float("inf") for y in range(GRID_Y) for x in range(GRID_X)}

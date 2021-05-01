"""Constants go here"""
import os
from collections import namedtuple

import pygame

from .settings import Settings

# Load Settings
settings = Settings('settings.json')

# Version
version = settings.version

# Last Loaded Alg
default_alg = settings.default_alg

# Supported Algs
WEIGHTED = [
    "astar",
    "dijkstra",
    "greedy"
]
unweighted = [
    "bfs",
    "dfs"
]

# Colors
Color = namedtuple('Color', ['r', 'g', 'b'])
PINK = Color(252, 15, 192)
DARK_PINK = Color(187, 0, 255)
RED = Color(255, 0, 0)
ORANGE = Color(255, 140, 0)
YELLOW = Color(255, 254, 106)
GREEN = Color(0, 255, 0)
LIGHT_BLUE = Color(175, 216, 248)
BLUE = Color(64, 206, 227)
DARK_BLUE = Color(15, 66, 88)
SEARCH_COLORS = (DARK_PINK, BLUE, YELLOW)
TARGET_COLORS = [RED, GREEN, PINK]

# Dark Mode
if settings.dark_mode:
    WHITE = DARK_MODE_WHITE = Color(100, 100, 100)
else:
    WHITE = LIGHT_MODE_WHITE = Color(255, 255, 255)

# Screen Properties
WIDTH, HEIGHT = settings.screen_size["WIDTH"], settings.screen_size["HEIGHT"]

# Grid Properties
GRID_X, GRID_Y = settings.grid_size["WIDTH"], settings.grid_size["HEIGHT"]
GRID_SIZE: tuple = GRID_X, GRID_Y
GRID_OFFSET: tuple = (GRID_X - 1, GRID_Y - 1)

# Node Properties
OFFSET = 3
NODE_SIZE = settings.node_size
WEIGHT_DENSITY: int = settings.weight_density
MAZE_DENSITY: float = settings.maze_density

# Load Spaceship
stretch_factor = (NODE_SIZE, NODE_SIZE)
SPACESHIP = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'spaceship.png')), stretch_factor)

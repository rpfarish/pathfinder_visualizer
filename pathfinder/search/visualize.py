"""Visualizes the Grid class"""
import time

import pygame

from pathfinder import settings
from pathfinder.constants import GREEN, ORANGE, PINK, RED, WEIGHTED, YELLOW
from pathfinder.node import Grid
from pathfinder.utils import key_lock


class Visualize:
    """Visualizes the path and search area"""

    keys_lock = [0] * 512

    cache = []
    objs = []

    def __init__(self, grid: Grid, start, end, end_color, alg, win, color,
                 search_speed, level, parent, searched):
        Visualize.objs.append(self)
        self.targets = [RED, GREEN, PINK]
        if alg in WEIGHTED:
            self.targets.append(ORANGE)
        self.speed = search_speed
        self._speed = search_speed
        self.grid = grid
        self.win = win
        self.alg = alg
        self.start = start
        self.end = end
        self.end_color = end_color
        self.level = level
        self.parent = parent
        self.area_color = color
        self.searched_nodes = searched

    def __getitem__(self, key):
        return self.grid[key]

    def __setitem__(self, key, value):
        self.grid[key] = value

    def __iter__(self):
        return iter(self.grid)

    def values(self):
        """:returns iterator of grid values"""
        return iter(self.grid.values())

    def items(self):
        """:returns iterator of grid items"""
        return iter(self.grid.items())

    def keys(self):
        """:returns iterator of grid keys"""
        return iter(self.grid.keys())

    def __len__(self):
        return len(self._get_path())

    def __repr__(self):
        return f"""{self.__class__.__name__}({self.grid}, {self.start}, {self.end},
                    {self.end_color}, {self.alg}, {self.win}, {self.area_color},
                    {self._speed}, {self.level}, {self.parent}, {self.searched_nodes})"""

    @staticmethod
    def pygame_quit(paused=False):
        """
        Allows the user to exit, to pause,
        keeps the window from freezing.
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE]:
            return True
        elif keys[pygame.K_ESCAPE]:
            quit()
        elif key_lock(keys, pygame.K_p, Visualize.keys_lock):
            paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            keys = pygame.key.get_pressed()
            if key_lock(keys, pygame.K_p, Visualize.keys_lock):
                break
            elif keys[pygame.K_BACKSPACE]:
                return None
            elif keys[pygame.K_ESCAPE]:
                quit()

        return False

    @property
    def search_speed(self):
        return self.speed if self.alg != 'dijkstra' else self.speed * .2

    def _render(self, node: Grid):
        """draws and then caches a node"""
        self[node].draw(self.win)
        self.cache.append(self[node].rect_obj)

    def _update(self, node, clear=False):
        """Renders and then updates the display"""
        self._render(node)
        pygame.display.update(self.cache)
        if clear:
            self.cache.clear()

    def _get_path(self):
        end_parent = self.parent[self.end]
        path = [end_parent]

        while True:
            end_parent = self.parent[end_parent]
            if end_parent is None:
                break
            else:
                path.append(end_parent)

        return path

    def _get_path_dict(self):
        if self.end not in self.parent:
            return {}
        end_parent = self.parent[self.end]
        path = {end_parent: YELLOW}

        while True:
            end_parent = self.parent[end_parent]
            if end_parent is None:
                break
            else:
                path[end_parent] = YELLOW

        return path

    def _draw_path_node(self, node):
        self[node].is_target = True
        self._update(node, clear=True)
        self[node].is_target = False
        time.sleep(settings.path_speed)
        self._render(node)

    def draw_both(self):
        """Visualizes the search area and draws the path"""
        area = {}
        for node in self.searched_nodes:
            if self[node].color == self.end_color:
                break
            if not self[node].is_path():
                area[node] = self.area_color

        both = area | self._get_path_dict()

        for node, color in both.items():
            if self[node].color not in self.targets:
                self[node].color = color
                self._render(node)

    def draw_path(self):
        """Visualizes the path"""
        if self.end in self.parent:

            for node in reversed(self._get_path()):
                if self.pygame_quit():
                    return

                if self[node].color not in self.targets:
                    self[node].color = YELLOW
                    self._draw_path_node(node)

                elif self[node].is_weight():
                    self._draw_path_node(node)

            pygame.display.update()

    def draw_search_area(self):
        """Draws the search area"""
        for node in self.searched_nodes:
            # allow user to exit
            if self.pygame_quit():
                return None

            # stop visualization if end was found
            if self[node].color == self.end_color:
                self._update(node, clear=True)
                return True

            elif self[node].color not in self.targets:

                self[node].color = YELLOW

                self._update(node, clear=True)
                time.sleep(self.search_speed)
                self[node].color = self.area_color
                self._render(node)

        print('No solution was found')
        return False

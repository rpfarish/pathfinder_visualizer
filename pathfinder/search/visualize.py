"""Visualizes the Grid class"""
import time
from math import log

import pygame

from pathfinder import settings
from pathfinder.constants import GREEN, ORANGE, PINK, RED, YELLOW
from pathfinder.node import Grid

used_keys = [pygame.K_p, pygame.K_SPACE]


def increment_keyslock(keys):
    for i in used_keys:
        if keys[i]:
            Visualize.keyslock[i] = 1
        else:
            Visualize.keyslock[i] = 0


def keylock(index, keys):
    if keys[index] and Visualize.keyslock[index] == 0:
        Visualize.keyslock[index] = 1
        return True
    else:
        return False


class Visualize:
    """
    visualizer class
    grid is an object of Grid
    """

    keyslock = [0 for _ in range(512)]

    cache = []
    objs = []

    def __init__(self, grid: Grid, start, end, end_color, alg, win, color,
                 search_speed, level, parent, searched):
        Visualize.objs.append(self)
        self.targets = [RED, GREEN, PINK]
        if alg in settings.weighted:
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
    def pygame_quit():
        """
        Allows the user to exit,
        keeps the window from freezing and
        silences the pygame display not init error
        """
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_BACKSPACE]:
                return True
            elif keys[pygame.K_ESCAPE]:
                raise SystemExit
            elif keylock(pygame.K_p, keys):
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                    keys = pygame.key.get_pressed()
                    if keylock(pygame.K_p, keys) or keylock(pygame.K_SPACE, keys):
                        break
                    elif keys[pygame.K_BACKSPACE]:
                        return None
                    elif keys[pygame.K_ESCAPE]:
                        raise SystemExit
                    increment_keyslock(keys)
            increment_keyslock(keys)

            return False
        except pygame.error:
            pass

    @property
    def search_speed(self):
        return self.speed if self.alg != 'dijkstra' else self.speed * .2

    def _render(self, node: Grid):
        """draws and then caches a node"""
        self[node].draw(self.win)
        self.cache.append(self[node].rect_obj)

    def _update(self, node, clear=False):
        """renders and then updates the display"""
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
        # time.sleep(1)
        time.sleep(0.07)
        self._render(node)

    def draw_both(self):
        area = {}
        for node in self.searched_nodes:
            if self[node].color == self.end_color:
                break
            if self[node].color != YELLOW:
                area[node] = self.area_color

        both = area | self._get_path_dict()

        for node, color in both.items():
            if self[node].color not in self.targets:
                self[node].color = color
                self._render(node)

    def draw_path(self):
        """visualizes the path"""
        if self.end in self.parent:

            for node in reversed(self._get_path()):
                if self.pygame_quit():
                    return

                if self[node].color not in self.targets:
                    self[node].color = YELLOW
                    self._draw_path_node(node)

                elif self[node].color == ORANGE:
                    self._draw_path_node(node)

            else:
                pygame.display.flip()

    def draw_search_area(self):
        """draws the search area"""
        for i, node in enumerate(self.searched_nodes, 1):
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
                time.sleep(self.search_speed * log(i, 8))
                self[node].color = self.area_color
                self._render(node)

        else:
            print('No solution was found')
            return False

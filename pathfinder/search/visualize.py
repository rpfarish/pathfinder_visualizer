"""Visualizes the Grid class"""
import time
from math import log

import pygame

from pathfinder.constants import green, orange, pink, red, weighted, yellow
from pathfinder.node import Grid


class Visualize:
    """
    visualizer class
    nodes is an object of Grid
    """

    cache = []

    def __init__(self, nodes: Grid, start, end, end_color, alg, win, color,
                 search_speed, level, parent, searched):
        self.targets = [red, green, pink]
        if alg in weighted:
            self.targets.append(orange)
        self.search_speed = search_speed
        self.nodes = nodes
        self.win = win
        self.alg = alg
        self.start = start
        self.end = end
        self.end_color = end_color
        self.level = level
        self.parent = parent
        self.area_color = color
        self.searched_nodes = searched
        self.tail = None
        nodes.visualized = True

    @staticmethod
    def pygame_quit():
        """
        Allows the user to exit
        and keeps the window from freezing
        silences the pygame display not init error
        """
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_BACKSPACE]:
                raise SystemExit
            elif keys[pygame.K_ESCAPE]:
                raise SystemExit
        except pygame.error:
            pass

    def search(self):
        """
        Calls the correct alg for visualization
        :returns: if solution found :type: bool
        """
        if self.alg == 'bfs' or self.alg == 'dfs':
            return self.visualize()
        elif self.alg == 'dijkstra' or self.alg == 'astar':
            return self.visualize()
        elif self.alg == 'greedy':
            return self.visualize()

    def _render(self, node: Grid):
        """draws and then caches a node"""
        self.nodes.grid[node].draw(self.win)
        self.cache.append(self.nodes.grid[node].rect_obj)

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

    def draw_path(self):
        """visualizes the path"""
        if self.end in self.parent:

            for node in reversed(self._get_path()):
                self.pygame_quit()

                if self.nodes.grid[node].color not in self.targets:
                    self.nodes.grid[node].color = yellow
                    self.nodes.grid[node].is_target = True
                    self._update(node, clear=True)
                    self.nodes.grid[node].is_target = False
                    # time.sleep(1)
                    time.sleep(0.08)
                    self._render(node)
            else:
                pygame.display.flip()

    def visualize(self):
        """draws the search area"""
        for i, node in enumerate(self.searched_nodes, 1):
            # allow user to exit
            self.pygame_quit()

            # stop visualization if end was found
            if self.nodes.grid[node].color == self.end_color:
                self._update(node, clear=True)
                return True

            elif self.nodes.grid[node].color not in self.targets:

                self.nodes.grid[node].color = yellow

                self._update(node, clear=True)
                time.sleep(self.search_speed * log(i, 8))
                self.nodes.grid[node].color = self.area_color
                self._render(node)

        else:
            print('No solution was found')
            return False

"""visualizes the grid"""
import time
from math import log

import pygame

from .constants import green, orange, pink, red, yellow
from .node import Grid


class Visualize:
    """
    visualizer class
    nodes is an object of Grid
    """
    targets = [red, green, pink, orange]
    cache = []

    # @logger
    def __init__(self, nodes: Grid, start, end, end_color, alg, win, color, search_speed, level, parent, searched):
        self.nodes = nodes
        self.search_speed = search_speed
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
        Allows the user to exit and keeps the window from freezing
        """
        try:
            for event_ in pygame.event.get():
                if event_.type == pygame.QUIT:
                    pygame.quit()
            keys_ = pygame.key.get_pressed()
            if keys_[pygame.K_BACKSPACE]:
                raise SystemExit
            if keys_[pygame.K_ESCAPE]:
                raise SystemExit
        except pygame.error:
            # the video system not initialized
            pass

    def call_alg(self):
        """
        Calls the correct alg for visualization
        :returns: if solution found :type: bool
        """
        if self.alg == 'bfs' or self.alg == 'dfs':
            return self.visualize()
        elif self.alg == 'dijkstra' or self.alg == 'astar' or self.alg == 'greedy':
            return self.visualize()

    def clear(self):
        """
         Sends a tuple of colors to clear
        """
        self.nodes.clear_searched(self.win, (self.area_color,))
        self.nodes.clear_searched(self.win, (yellow,))

    def render(self, node: Grid):
        """
        Draws and then caches a node
        :param node:
        """
        self.nodes.grid[node].draw(self.win)
        self.cache.append(self.nodes.grid[node].rect_obj)

    def update(self, node, clear=False):
        """
        Renders and then updates the display
        :param node:
        :param clear:
        """
        self.render(node)
        pygame.display.update(self.cache)
        if clear:
            self.cache.clear()

    def draw_path(self):
        """
        Visualizes the path
        """
        if self.end in self.parent:
            end_node = self.end
            end_parent = self.parent[end_node]
            path = [end_parent]

            # find the shortest path starting at the end node in the parent dictionary
            while end_parent is not None:
                end_parent = self.parent[end_parent]
                path.append(end_parent)

            for i in reversed(range(len(path)-2)):
                self.pygame_quit()
                node = path[i]
                if self.nodes.grid[node].color not in self.targets:
                    self.nodes.grid[node].color = yellow
                    self.update(node)
                    time.sleep(0.08)

    def visualize(self):
        """
        Draws the search area
        """
        for i, node in enumerate(self.searched_nodes, 1):
            # allow user to exit
            self.pygame_quit()

            # stop visualization if end was found
            if self.nodes.grid[node].color == self.end_color:
                self.update(node, clear=True)
                return True
            elif self.nodes.grid[node].color not in self.targets:

                self.nodes.grid[node].color = yellow

                self.update(node, clear=True)
                time.sleep(self.search_speed * log(i, 8))
                self.nodes.grid[node].color = self.area_color
                self.render(node)
                # self.update(node, sleep=True)
                # time.sleep(self.search_speed)
        else:
            print('No solution was found')
            return False

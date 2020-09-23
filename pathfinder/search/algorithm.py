"""API to access and run the main path search"""
from pathfinder.algorithms import *
from pathfinder.constants import SEARCH_COLORS, search_speed, yellow
from pathfinder.node import Grid
from pathfinder.utils import timer
from .visualize import Visualize


class Algorithm:
    """
    Main API to access the pathfinder alg
    :param alg: algorithm to use to search with
    :param node_list: order of nodes to visit 
    :param walls: walls or obstructions in the grid
    :param grid_size: an int tuple of the size of the grid
    :param weights: weighed nodes in the grid
    """
    unweighted_funcs = {'bfs': bfs, 'dfs': dfs}
    weighted_funcs = {'astar': astar, 'dijkstra': dijkstra, 'greedy': greedy}

    unweighted = ['bfs', 'dfs']
    weighted = ['astar', 'dijkstra', 'greedy']

    def __init__(self, alg, node_list, walls, grid_size, weights):
        self.alg = alg
        self.node_list = node_list
        self.walls = walls
        self.grid_size = grid_size
        self.weights = weights
        self.node_count = 0
        self.clear_colors = []
        self.area = []
        self.visualize_objs = []

    @property
    def _start(self):
        return self.node_list[self.node_count]

    @property
    def _end(self):
        return self.node_list[self.node_count + 1]

    @timer
    def _get_search_data(self):
        """:returns result of the search"""

        if self._start != (None, None) and self._end != (None, None):
            if self.alg in self.unweighted:
                return self._call_unweighted()

            elif self.alg in self.weighted:
                return self._call_weighted()

    def _call_unweighted(self):
        return self.unweighted_funcs[self.alg](self._start, self._end, self.walls, self.grid_size)

    def _call_weighted(self):
        return self.weighted_funcs[self.alg](self._start, self._end, self.walls, self.grid_size, self.weights)

    def _get_visualize(self, win, graph, area_color, level, parent, searched):
        """:returns an instance of Visualize class"""
        return Visualize(graph, self._start, self._end, graph.grid[self._end].color,
                         self.alg, win, area_color, search_speed, level, parent, searched)

    def run_alg(self, win, graph: Grid, area_color):
        """searches and then visualizes the area and path"""
        self.clear_colors = SEARCH_COLORS
        self._clear(win, graph)
        for i in range(len(self.node_list) - 1):
            v = self._get_visualize(win, graph, area_color[i], *self._get_search_data())
            self.visualize_objs.append(v)
            self.node_count += 1
        else:
            # visualize area
            for node in self.visualize_objs:
                node.search()

            # draw path
            for node in self.visualize_objs:
                node.draw_path()
            self.node_count = 0

    def _clear(self, win, graph):
        """calls to class Grid to clear """
        for color in self.clear_colors:
            graph.clear_searched(win, (color,))
        else:
            graph.clear_searched(win, (yellow,))

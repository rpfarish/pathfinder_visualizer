"""API to access and run the main path search"""

from pathfinder.algorithms import *
from pathfinder.constants import SEARCH_COLORS, YELLOW
from pathfinder.node import Grid
from pathfinder.utils import timer
from .visualize import Visualize
from .. import settings


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

    def __init__(self, alg, node_list, grid_size, walls, weights):
        self.alg = alg
        self.node_list = node_list
        self.grid_size = grid_size
        self.walls = walls
        self.weights = weights
        self.node_count = 0
        self.clear_colors = []
        self.area = []
        self.vis_objs = []

    @property
    def _start(self):
        return self.node_list[self.node_count]

    @property
    def _end(self):
        return self.node_list[self.node_count + 1]

    @timer
    def _get_search_data(self):
        """:returns result of the search"""

        if self.alg in self.unweighted_funcs:
            return self._call_unweighted()

        elif self.alg in self.weighted_funcs:
            return self._call_weighted()

    @property
    def _unweighted_params(self):
        return self._start, self._end, self.walls, self.grid_size

    def _call_unweighted(self):
        return self.unweighted_funcs[self.alg](*self._unweighted_params)

    def _call_weighted(self):
        return self.weighted_funcs[self.alg](*self._unweighted_params, self.weights)

    def __call__(self, win, graph: Grid, area_color):
        """searches and then visualizes the area and path"""
        self.clear_colors = SEARCH_COLORS
        self._clear(win, graph)
        for i in range(len(self.node_list) - 1):
            # do the search with the alg and get the result
            node_score, parent, visited = self._get_search_data()

            # cache visualizable object
            Visualize(graph, self._start, self._end, graph.grid[self._end].color,
                      self.alg, win, area_color[i], settings.search_speed, node_score, parent, visited)

            self.node_count += 1
        else:
            # visualize area
            for vis in Visualize.objs:
                end_found = vis.draw_search_area()
                if not end_found:
                    Visualize.objs.clear()
                    return

            # draw path
            for vis in Visualize.objs:
                vis.draw_path()
                print(len(vis))

            self.node_count = 0
            Visualize.objs.clear()

    def _clear(self, win, graph):
        """calls to class Grid to clear """
        for color in self.clear_colors:
            graph.clear_searched(win, (color,))
        else:
            graph.clear_searched(win, (YELLOW,))

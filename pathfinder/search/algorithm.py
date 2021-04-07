"""API to access and run the main path search"""

from pathfinder.algorithms import *
from pathfinder.constants import SEARCH_COLORS, YELLOW
from pathfinder.node import Grid
from .visualize import Visualize
from .. import settings


class Algorithm:
    """
    Main API to access the pathfinder alg
    :param alg: algorithm to use to search with
    :param node_list: order of nodes to visit 
    :param grid_size: an int tuple of the size of the grid
    :param walls: walls or obstructions in the grid
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

    @property
    def _start(self):
        return self.node_list[self.node_count]

    @property
    def _end(self):
        return self.node_list[self.node_count + 1]

    # @timer
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

    def __call__(self, win, graph: Grid, area_color, auto=False):
        """
        searches and then visualizes the graph structure
        in order of the nodes in node_list then draws the path
        """

        self._clear(win, graph, update=not auto)

        for i in range(len(self.node_list) - 1):
            # do the search with the alg and get the result
            node_score, parent, visited = self._get_search_data()

            # cache visualizable object
            Visualize(graph, self._start, self._end, graph[self._end].color,
                      self.alg, win, area_color[i], settings.search_speed, node_score, parent, visited)

            self.node_count += 1

        if auto:
            for vis in Visualize.objs:
                vis.draw_both()
        else:
            # draw each graph search
            for vis in Visualize.objs:
                end_found = vis.draw_search_area()
                if not end_found:
                    break
            else:
                # draw each path
                for vis in Visualize.objs:
                    vis.draw_path()
                    # print(len(vis))

        self.node_count = 0
        Visualize.objs.clear()

    def _clear(self, win, graph, update=True):
        """calls to class Grid to clear """

        for color in SEARCH_COLORS:
            graph.clear_searched(win, (color,), update)
        else:
            graph.clear_searched(win, (YELLOW,), update)

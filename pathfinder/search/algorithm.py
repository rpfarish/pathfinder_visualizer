"""API to access and run the main path search"""
from pathfinder.algorithms.astar import astar
from pathfinder.algorithms.bfs import bfs
from pathfinder.algorithms.dfs import dfs
from pathfinder.algorithms.dijkstra import dijkstra
from pathfinder.algorithms.greedy import greedy
from pathfinder.constants import search_speed, yellow
from pathfinder.visualize import Visualize


class Algorithm:
    """
    Main API to access the pathfinder alg
    :param alg: algorithm to use to search with

    :param walls: walls or obstructions in the grid
    :param grid_size: an int tuple of the size of the grid
    """
    unweighted_funcs = {'bfs': bfs, 'dfs': dfs}
    weighted_funcs = {'astar': astar, 'dijkstra': dijkstra, 'greedy': greedy}

    unweighted = ['bfs', 'dfs']
    weighted = ['astar', 'dijkstra', 'greedy']

    # @logger
    def __init__(self, alg, node_list, walls, grid_size, weights):
        self.alg = alg
        self.node_list = node_list
        self.walls = walls
        self.grid_size = grid_size
        self.weights = weights
        self.node_count = 0
        self.clear_colors = []
        self.paths = []

    def visualize(self, win, graph, area_color, level, parent, searched):
        """

        :param win:
        :param graph:
        :param area_color:
        :param level:
        :param parent:
        :param searched:
        :return:
        """
        v = Visualize(graph, self.start, self.end, graph.grid[self.end].color, self.alg, win, area_color, search_speed,
                      level, parent,
                      searched)

        v.call_alg()
        return v.draw_path

    @property
    def start(self):
        """

        :return:
        """
        return self.node_list[self.node_count]

    @property
    def end(self):
        """

        :return:
        """
        return self.node_list[self.node_count + 1]

    def run_alg(self, win, graph, area_color):
        """

        :param win:
        :param graph:
        :param area_color:
        """
        self.clear_colors = area_color
        self.clear(win, graph)
        for i in range(len(self.node_list) - 1):
            path = self.visualize(win, graph, area_color[i], *self.call_alg())
            self.paths.append(path)
            self.node_count += 1
        else:
            for p in self.paths:
                p()
            self.node_count = 0

    def clear(self, win, graph):
        """

        :param win:
        :param graph:
        """
        for color in self.clear_colors:
            graph.clear_searched(win, (color,))
        else:
            graph.clear_searched(win, (yellow,))

    def call_alg(self):
        """
        calls pathfinder alg
        :returns the alg used, result of the search
        """

        if self.alg in self.unweighted:
            return self.call_unweighted()

        elif self.alg in self.weighted:
            # todo this is the spot that you would implement bomb
            return self.call_weighted()

    def call_unweighted(self):
        """

        :return:
        """
        if self.start != (None, None) and self.end != (None, None):
            return self.unweighted_funcs[self.alg](self.start, self.end, self.walls, self.grid_size)

    def call_weighted(self):
        """

        :return:
        """
        if self.start != (None, None) and self.end != (None, None):
            return self.weighted_funcs[self.alg](self.start, self.end, self.walls, self.grid_size, self.weights)

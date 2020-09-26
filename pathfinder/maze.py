"""Maze generation"""
from random import randrange

from .constants import TARGET_COLORS, green, pink, red
from .node import Grid


def _clear(win, graph: Grid):
    graph.clear(win, reset_targets=False)


class Maze:
    """Constructs Mazes"""

    def __init__(self, grid_x, grid_y):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.node_colors = [red, green, pink]

    def basic_random_maze(self, win, graph: Grid):
        """Basic random distribution maze"""
        _clear(win, graph)
        for x in range(self.grid_x):
            for y in range(self.grid_y):
                if graph.grid[(x, y)].color not in TARGET_COLORS:
                    if randrange(0, 100) < 30:
                        graph.grid[(x, y)].make_wall()
        else:
            graph.draw_grid(win)
    #
    # def basic_weight_maze(self, win, graph: Grid):
    #     """Basic random distribution maze"""
    #     _clear(win, graph, SEARCH_COLORS)
    #     _clear(win, graph, orange)
    #     for x in range(self.grid_x):
    #         for y in range(self.grid_y):
    #             if graph.grid[(x, y)].color not in TARGET_COLORS:
    #                 if randrange(0, 100) < 30:
    #                     graph.grid[(x, y)].make_weight()
    #
    #     else:
    #         graph.draw_grid(win)

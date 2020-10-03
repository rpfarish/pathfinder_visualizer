"""Maze generation"""
from random import randrange

from .algorithms import greedy
from .constants import GREEN, PINK, RED, TARGET_COLORS
from .node import Grid


def _clear(win, graph: Grid):
    graph.clear(win, reset_targets=False)


class Maze:
    """Constructs Mazes"""

    def __init__(self, grid_size):
        self.grid_x, self.grid_y = grid_size

        self.node_colors = [RED, GREEN, PINK]

    def waypoint(self, graph, start, end):
        """:returns if there is a path between start and end"""
        score, *_ = greedy(start, end, graph.walls,
                           (self.grid_x - 1, self.grid_y - 1), graph.weights)

        return False if score[end] == float('inf') else True

    def has_solution(self, graph):
        """:returns if there is a path between all nodes on graph"""
        if graph.has_bomb:
            return True if self.waypoint(graph, graph.start, graph.bomb) \
                           and self.waypoint(graph, graph.bomb, graph.end) else False

        return True if self.waypoint(graph, graph.start, graph.end) else False

    def basic_random_maze(self, win, graph: Grid):
        """Basic random distribution maze"""
        _clear(win, graph)
        for x in range(self.grid_x):
            for y in range(self.grid_y):
                if graph.grid[(x, y)].color not in TARGET_COLORS:
                    if randrange(0, 100) < 30:
                        graph.grid[(x, y)].make_wall()
        else:
            if self.has_solution(graph):
                graph.draw_grid(win)
            else:
                self.basic_random_maze(win, graph)

    def basic_weight_maze(self, win, graph: Grid):
        """Basic random distribution maze"""
        _clear(win, graph)
        for x in range(self.grid_x):
            for y in range(self.grid_y):
                if graph.grid[(x, y)].color not in TARGET_COLORS:
                    if randrange(0, 100) < 30:
                        graph.grid[(x, y)].make_weight()
        else:
            graph.draw_grid(win)

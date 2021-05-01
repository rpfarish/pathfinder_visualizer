"""Maze generation"""
import random

from .algorithms import greedy
from .constants import GRID_OFFSET, GRID_SIZE, MAZE_DENSITY, TARGET_COLORS
from .node import Grid


def _clear(win, graph: Grid):
    graph.clear(win, reset_targets=False)


class Maze:
    """Constructs Mazes"""

    def __init__(self):
        self.grid_x, self.grid_y = GRID_SIZE

    @property
    def can_place_wall(self) -> bool:
        """
        :returns if a wall can be placed based
        on the maze density percentage
        """
        return random.uniform(0, 1) < MAZE_DENSITY

    @staticmethod
    def is_connected(graph, start, end):
        """:returns if there is a path between start and end"""
        score, *_ = greedy(start, end, graph.walls, GRID_OFFSET, graph.weights)
        return False if score[end] == float('inf') else True

    def has_solution(self, graph):
        """:returns if there is a path between all nodes on graph"""
        if graph.has_bomb:
            start_to_bomb = self.is_connected(graph, graph.start, graph.bomb)
            bomb_to_end = self.is_connected(graph, graph.bomb, graph.end)
            if start_to_bomb and bomb_to_end:
                return True
        return True if self.is_connected(graph, graph.start, graph.end) else False

    def basic_random_maze(self, win, graph: Grid):
        """Basic random maze"""
        _clear(win, graph)
        for x in range(self.grid_x):
            for y in range(self.grid_y):
                if self.can_place_wall and graph[(x, y)].color not in TARGET_COLORS:
                    graph[(x, y)].make_wall()

        if self.has_solution(graph):
            graph.draw_grid(win)
        else:
            self.basic_random_maze(win, graph)

    def basic_weight_maze(self, win, graph: Grid):
        """Basic random weight maze"""
        _clear(win, graph)
        for x in range(self.grid_x):
            for y in range(self.grid_y):
                if self.can_place_wall and graph[(x, y)].color not in TARGET_COLORS:
                    graph[(x, y)].make_weight()

        graph.draw_grid(win)

"""Maze generation"""
import random

from .algorithms import greedy
from .constants import GRID_OFFSET, GRID_SIZE
from .constants import MAZE_DENSITY_PERCENTAGE, TARGET_COLORS
from .node import Grid


class Maze:
    """Constructs Mazes"""

    def __init__(self):
        self.grid_x, self.grid_y = GRID_SIZE

    @property
    def _can_place_wall(self) -> bool:
        """:returns if a wall can be placed based on a density percentage"""
        return random.uniform(0, 1) < MAZE_DENSITY_PERCENTAGE

    @staticmethod
    def _clear(win, graph: Grid):
        graph.clear(win, reset_targets=False)

    @staticmethod
    def _is_connected(graph, start, end) -> bool:
        """:returns if there is a path between start and end"""
        score, *_ = greedy(start, end, graph.walls, GRID_OFFSET, graph.weights)
        return score[end] != float('inf')

    def _has_solution(self, graph) -> bool:
        """:returns if there is a path between all target nodes on graph"""
        if graph.has_bomb:
            start_to_bomb = self._is_connected(graph, graph.start, graph.bomb)
            bomb_to_end = self._is_connected(graph, graph.bomb, graph.end)
            return start_to_bomb and bomb_to_end

        return self._is_connected(graph, graph.start, graph.end)

    def basic_random_maze(self, win, graph: Grid):
        """Generates a basic random maze"""
        self._clear(win, graph)

        for x in range(self.grid_x):
            for y in range(self.grid_y):
                is_target = graph[(x, y)].color in TARGET_COLORS
                if self._can_place_wall and not is_target:
                    graph[(x, y)].make_wall()
        if self._has_solution(graph):
            graph.draw_grid(win)
        else:
            self.basic_random_maze(win, graph)

    def basic_weight_maze(self, win, graph: Grid):
        """Generates a basic random weight maze"""
        self._clear(win, graph)

        for x in range(self.grid_x):
            for y in range(self.grid_y):
                is_target = graph[(x, y)].color in TARGET_COLORS
                if self._can_place_wall and not is_target:
                    graph[(x, y)].make_weight()

        graph.draw_grid(win)

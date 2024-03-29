"""returns a list of all adjacent nodes"""
import numpy as np

from pathfinder import settings
from pathfinder.utils import cache


@cache
def h(p1, p2):
    """Manhattan distance"""
    (x1, y1), (x2, y2) = p1, p2
    return abs(x1 - x2) + abs(y1 - y2)


def adjacent_nodes(node: tuple, wall, grid_size):
    """
    Gets the adjacent nodes of the current node within the bounds of the grid and excludes walls.
    If diagonals are enabled, it then joins the adjacent nodes to the diagonal nodes.
    :param node: node coordinate
    :param wall: list of walls
    :param grid_size: a tuple eg (3, 2)
    """
    if node in wall:
        return {}
    adj = {}
    x, y = node
    if 0 < x and (x - 1, y) not in wall:
        adj[(x - 1, y)] = 1  # LEFT
    if x < grid_size[0] and (x + 1, y) not in wall:
        adj[(x + 1, y)] = 1  # RIGHT
    if 0 < y and (x, y - 1) not in wall:
        adj[(x, y - 1)] = 1  # UP
    if y < grid_size[1] and (x, y + 1) not in wall:
        adj[(x, y + 1)] = 1  # DOWN
    if settings.enable_diagonals:
        adj |= adjacent_diagonals(node, wall, grid_size)
    return adj


def adjacent_diagonals(node, wall, grid_size):
    """
    Supports diagonals using rotation via matrix multiplication
    :param node: node coordinate
    :param wall: list of walls
    :param grid_size: a tuple eg (3, 2)
    """
    adjacent = {}
    rotation = np.array([[0, 1], [-1, 0]])  # clockwise 90-degrees
    # Calculate the adj node in the form:
    # adjacent := Node + AY (where A is the rotation, Y is the initial direction and all three are matrices)

    direction = np.array([1, 1])  # diagonal up-right
    for angle in range(4):
        rotated_vector = np.matmul(direction, np.linalg.matrix_power(rotation, angle))
        x, y = potential_node = tuple(np.add(node, rotated_vector))
        if potential_node not in wall and 0 <= x <= grid_size[0] and 0 <= y <= grid_size[1]:
            adjacent[potential_node] = np.sqrt(2)

    return adjacent

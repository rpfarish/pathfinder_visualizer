"""The Breadth-First Search Algorithm"""
from .adjacent_nodes import adjacent_nodes


def bfs(start, end, wall, grid_size):
    """
    Define a nodes location as a tuple e.g. (3,4) and (2,4),
        and a node is adjacent if it can be reached by moving either x or y by |1| away (1 or -1).
    """
    level = {start: 0}
    parent = {start: None}
    i = 1
    searched_nodes = []
    current_level_nodes = [start]
    while current_level_nodes:
        next_level = []
        for node in current_level_nodes:
            searched_nodes.append(node)
            if end == node:
                return level, parent, searched_nodes
            for adjacent in adjacent_nodes(node, wall, grid_size):
                if adjacent not in level:
                    level[adjacent] = i
                    parent[adjacent] = node
                    next_level.append(adjacent)

        else:
            current_level_nodes = next_level
            i += 1

    level[end] = float('inf')
    return level, parent, searched_nodes

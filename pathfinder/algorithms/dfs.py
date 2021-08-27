"""Depth-First Search"""
from pathfinder.utils import cache
from .adjacent_nodes import adjacent_nodes


@cache
def dfs(start, end, wall, grid_size):
    """Depth-First Search"""
    stack = [start]
    visited = []
    parent = {start: None}
    level = {}
    for x in range(grid_size[0] + 1):
        for y in range(grid_size[1] + 1):
            if (x, y) not in wall:
                level[(x, y)] = float('inf')
    while stack:
        curr = stack.pop()

        if curr not in visited:
            visited.append(curr)

        if curr == end:
            level[end] = 1
            return level, parent, visited

        for adj in adjacent_nodes(curr, wall, grid_size):
            if adj not in visited:
                stack.append(adj)
                parent[adj] = curr

    return level, parent, visited

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


if __name__ == "__main__":
    _start = (0, 0)
    _end = (3, 1)
    a, _parent, c = dfs(_start, _end, [(1, 1), (1, 2), (0, 2)], (5, 5))
    ra = a[::-1]

    if _end in _parent:
        end_parent = _parent[_end]
        path = [end_parent]
        while end_parent is not None:
            end_parent = _parent[end_parent]
            path.append(end_parent)
        print(ra)
        print(path)

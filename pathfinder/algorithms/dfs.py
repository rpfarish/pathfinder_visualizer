"""dfs"""
from pathfinder.search.adjacent_nodes import adjacent_nodes

# def bfs(start, end, wall, grid_size):
def dfs(start, end, wall, grid_size):
    """dfs"""
    stack = [start]
    visited = []
    parent = {start: None}
    level = {}
    for x in range(grid_size[0] + 1):
        for y in range(grid_size[1] + 1):
            if (x, y) not in wall:
                level[(x, y)] = 1
    while stack:
        curr = stack.pop()

        if curr not in visited:
            visited.append(curr)

        if curr == end:
            return level, parent, visited

        for adj in adjacent_nodes(curr, wall, grid_size):
            if adj not in visited:
                stack.append(adj)
                parent[adj] = curr

    return level, parent, visited

# return level, parent, searched_nodes

if __name__ == "__main__":
    a, parent, c = dfs((0, 0), [(1, 1), (1, 2), (0, 2)], (5, 5), (3, 1))
    ra = a[::-1]
    start = (0, 0)
    end = (3, 1)

    if end in parent:
        end_parent = parent[end]
        path = [end_parent]
        while end_parent is not None:
            end_parent = parent[end_parent]
            path.append(end_parent)
        print(ra)
        print(path)

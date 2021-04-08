from queue import PriorityQueue

from pathfinder.constants import THE_GRID
from pathfinder.utils import cache
from .adjacent_nodes import adjacent_nodes


@cache
def dijkstra(start, end, wall, grid_size, weight_li):
    """
    The famous Dijkstra's Algorithm invented by Edsger Dijkstra and
    implemented with a priority queue.
    Non-weighted nodes have a default weight of 1 and diagonal nodes
    have a weight of square root of 2 when diagonals are enabled.
    """
    grid = THE_GRID.copy()
    prev = {start: None}
    queue = PriorityQueue()

    for i in THE_GRID:
        if i in wall:
            grid.pop(i)

    queue.put((0, start))
    grid[start] = 0
    visited = []
    while not queue.empty():
        curr_dist, curr = queue.get()

        if curr is None or curr == end:
            break

        adj_nodes = adjacent_nodes(curr, wall, grid_size)

        for adj in adj_nodes:
            pot_dist = curr_dist + weight_li[adj]
            pot_dist += adj_nodes[adj]  # diagonal weight
            if pot_dist < grid[adj]:
                grid[adj] = pot_dist
                prev[adj] = curr
            if adj not in visited:
                visited.append(adj)
                queue.put((pot_dist, adj))

    return grid, prev, visited


if __name__ == "__main__":
    print(dijkstra((0, 0), (6, 6), [], (10 - 1, 10 - 1), {(i, j): 1 for j in range(10) for i in range(10)}))

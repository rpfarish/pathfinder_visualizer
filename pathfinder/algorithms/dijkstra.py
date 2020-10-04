from queue import PriorityQueue

from pathfinder.constants import THE_GRID
from pathfinder.utils import cache
from .adjacent_nodes import adjacent_nodes


@cache
def dijkstra(start, end, wall, grid_size, weight_li):
    """
    The famous Dijkstra's Algorithm invented by Edsger Dijkstra and
    implemented with a priority queue.
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

        for adj in adjacent_nodes(curr, wall, grid_size):
            pot_dist = curr_dist + weight_li[adj]
            if pot_dist < grid[adj]:
                if adj not in visited:
                    visited.append(adj)
                    queue.put((pot_dist, adj))
                grid[adj] = pot_dist
                prev[adj] = curr
    return grid, prev, visited


if __name__ == "__main__":
    print(dijkstra((0, 0), (6, 6), [], (10 - 1, 10 - 1), {(i, j): 1 for j in range(10) for i in range(10)}))

"""The Greedy Best-first Search"""
from queue import PriorityQueue

from .adjacent_nodes import adjacent_nodes, h
from ..utils import cache


@cache
def greedy(start, end, wall, grid_size, weight_li):
    """The Greedy Best-first Search"""
    open_set = PriorityQueue()
    open_set.put((0, start))
    parent = {start: None}
    g_score = {}
    f_score = {}

    for x in range(grid_size[0] + 1):
        for y in range(grid_size[1] + 1):
            g_score[(x, y)] = float("inf")
            f_score[(x, y)] = float("inf")

    g_score[start] = 0
    f_score[start] = h(start, end)

    open_set_hash = {start}

    visited = []
    while not open_set.empty():

        current = open_set.get()[1]
        open_set_hash.remove(current)

        if current == end:
            break

        for adj in adjacent_nodes(current, wall, grid_size):
            pot_g_score = g_score[current] + (weight := weight_li[adj])

            if pot_g_score < g_score[adj]:
                if adj not in visited:
                    visited.append(adj)
                parent[adj] = current
                g_score[adj] = pot_g_score
                f_score[adj] = pot_g_score + (h_score := h(adj, end))
                if adj not in open_set_hash:
                    open_set.put((h_score + weight, adj))
                    open_set_hash.add(adj)
    return f_score, parent, visited

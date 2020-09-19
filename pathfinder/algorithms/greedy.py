"""The greedy algorithm"""
from queue import PriorityQueue

from pathfinder.search.adjacent_nodes import adjacent_nodes


def h(p1, p2):
    """
    manhattan distance
    :param p1:
    :param p2:
    :return:
    """
    (x1, y1), (x2, y2) = p1, p2
    return abs(x1 - x2) + abs(y1 - y2)


def greedy(start, end, wall, grid_size, weight_li):
    """the Greedy Best-first Search"""
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {start: None}
    g_score = {}
    f_score = {}

    for row in range(grid_size[0] + 1):
        for col in range(grid_size[1] + 1):
            g_score[(row, col)] = float("inf")
            f_score[(row, col)] = float("inf")

    g_score[start] = 0
    f_score[start] = h(start, end)

    open_set_hash = {start}

    visit_order = []
    while not open_set.empty():

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            break

        for adjacent in adjacent_nodes(current, wall, grid_size):
            temp_g_score = g_score[current] + weight_li[adjacent]
            if adjacent not in visit_order:
                visit_order.append(adjacent)

            if temp_g_score < g_score[adjacent]:
                came_from[adjacent] = current
                g_score[adjacent] = temp_g_score
                f_score[adjacent] = temp_g_score + h(adjacent, end)
                if adjacent not in open_set_hash:
                    count += 1
                    open_set.put((h(adjacent, end) + weight_li[adjacent], count, adjacent))
                    open_set_hash.add(adjacent)
    return f_score, came_from, visit_order

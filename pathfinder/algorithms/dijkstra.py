from pathfinder.search.adjacent_nodes import adjacent_nodes


def min_of_grid_in_check_node(grid, check_node):
    seq = {i: grid[i] for i in check_node}
    node = float("inf")
    a, b = None, None
    for key, val in seq.items():
        if val < node:
            node = val
            a = key
            b = val
    return a, b


def dijkstra(start, end, wall, grid_size,  weight_li):
    """TODO put check node in a PriorityQueue"""
    grid = {}
    check_node = []
    prev = {start: None}
    for x in range(grid_size[0] + 1):
        for y in range(grid_size[1] + 1):
            if (x, y) not in wall:
                check_node.append((x, y))
            grid[(x, y)] = float("inf")

    grid[start] = 0
    visit_order = []
    while check_node:
        curr, curr_dist = min_of_grid_in_check_node(grid, check_node)
        if curr is None or curr == end:
            break

        check_node.remove(curr)
        for adj in adjacent_nodes(curr, wall, grid_size):
            pot_dist = curr_dist + weight_li[adj]
            if pot_dist < grid[adj]:
                if adj not in visit_order:
                    visit_order.append(adj)
                grid[adj] = pot_dist
                prev[adj] = curr
    return grid, prev, visit_order


if __name__ == "__main__":
    print(dijkstra((0, 0), (6, 6), [], (10-1, 10-1),  {(i, j): 1 for j in range(10) for i in range(10)}))

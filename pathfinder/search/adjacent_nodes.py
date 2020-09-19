"""returns a list of all adjacent nodes"""


def adjacent_nodes(node, wall, grid_size):
    """
    :param node: node coordinate
    :param wall: list of walls
    :param grid_size: a tuple eg (3, 2)
    """
    adj = []
    x, y = node
    if 0 < x and (x - 1, y) not in wall:
        adj.append((x - 1, y))  # LEFT
    if x < grid_size[0] and (x + 1, y) not in wall:
        adj.append((x + 1, y))  # RIGHT
    if 0 < y and (x, y - 1) not in wall:
        adj.append((x, y - 1))  # UP
    if y < grid_size[1] and (x, y + 1) not in wall:
        adj.append((x, y + 1))  # DOWN

    return adj if node not in wall else []

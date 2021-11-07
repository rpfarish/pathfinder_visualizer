"""Pathfinder Visualizer Project"""
from typing import Sequence

import pygame
from pygame.surface import Surface

import pathfinder as pf
from pathfinder.maze import Maze
from pathfinder.node import Grid
from pathfinder.search import Algorithm
from pathfinder.utils import get_node_pos, key_lock

# WINDOW SETUP
WIN = pygame.display.set_mode((pf.WIDTH, pf.HEIGHT))
pygame.display.set_caption(f"Pathfinder v{pf.version}")


def redraw_window(win: Surface):
    """Updates the entire screen"""
    WIN.fill(pf.LIGHT_BLUE)
    graph.draw_grid(win)
    pygame.display.update()


def update_nodes():
    """Updates objects that have changed states"""
    pygame.display.update()
    Grid.cache.clear()


def run_search(win: Surface, graph_: Grid, auto=False):
    """
    Calls the Algorithm class to visualize
    the pathfinder algorithm using the Visualize class
    """
    print('Visualization started with:', pf.settings.default_alg.title())
    if not graph_.has_bomb:
        node_list = [graph_.start, graph_.end]
        search_colors = [pf.BLUE]
    else:
        node_list = [graph_.start, graph_.bomb, graph_.end]
        search_colors = [pf.DARK_PINK, pf.BLUE]

    alg = Algorithm(pf.settings.default_alg, node_list, pf.GRID_OFFSET,
                    graph_.walls, graph_.weights)
    alg(win, graph_, search_colors, auto)
    print('Visualization done')


def set_alg(_keys: Sequence[bool], alg_map_: dict[int:str]):
    """Sets the alg using keys and alg_map instead of multiple else ifs"""
    shift_ = (_keys[pygame.K_LSHIFT] or _keys[pygame.K_RSHIFT])
    if not shift_:
        return
    for key, new_alg in alg_map_.items():
        if _keys[key]:
            pf.settings.default_alg = new_alg
            graph.reset_visualization(WIN)
            graph.visualized = False
            break


# SETUP VARIABLES
graph = Grid(WIN)
maze = Maze()
key_prev_states = [0] * 512
curr_node_temp = None
dragging = False
running = True
redraw_window(WIN)
clock = pygame.time.Clock()

# used to avoid else-ifs
alg_map = {
    pygame.K_a: 'astar',
    pygame.K_b: 'bfs',
    pygame.K_f: 'dfs',
    pygame.K_d: 'dijkstra',
    pygame.K_g: 'greedy',
}

# MAIN LOOP
while running:

    # UPDATE STATES
    update_nodes()
    clock.tick(2000)

    mouse = pygame.mouse.get_pos()
    left_click, _, right_click = pygame.mouse.get_pressed(num_buttons=3)
    curr_node = get_node_pos(graph, mouse)  # Node hovered by mouse

    keys = pygame.key.get_pressed()
    shift = (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT])

    set_alg(keys, alg_map)  # Change current alg

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    # DRAGGABLE NODES
    if curr_node in graph.draggable:
        if left_click:
            dragging = True
            curr_node_temp = curr_node

    if not left_click:
        dragging = False

    if dragging:
        # Prevent start and end nodes from being dragged onto each other
        if curr_node == graph.start and curr_node_temp == graph.end:
            continue

        if curr_node_temp != curr_node:
            graph.set_drag_state(WIN, curr_node_temp, curr_node)
            curr_node_temp = curr_node

        if graph.visualized:
            run_search(WIN, graph, auto=True)

        continue

    # SET AND CLEAR NODES
    if left_click and not any(keys) and curr_node not in graph.draggable:
        graph.set_wall(WIN, curr_node)
        continue

    elif keys[pygame.K_b] and left_click and not graph.has_bomb:
        graph.set_bomb(WIN, curr_node)

    elif keys[pygame.K_w] and left_click:
        graph.set_weight(WIN, curr_node, pf.settings.default_alg)
        continue

    elif right_click and curr_node not in (graph.end, graph.start):
        graph.clear_node(WIN, curr_node, True)

    # SET MAZES
    elif shift and key_lock(keys, pygame.K_m, key_prev_states):
        if pf.settings.default_alg in pf.WEIGHTED:
            maze.basic_weight_maze(WIN, graph)
            redraw_window(WIN)
            graph.visualized = False

    elif key_lock(keys, pygame.K_m, key_prev_states):
        maze.basic_random_maze(WIN, graph)
        redraw_window(WIN)
        graph.visualized = False

    # RESET GRAPH
    elif keys[pygame.K_c]:
        graph.clear(WIN)
        graph.visualized = False

    # QUIT
    elif keys[pygame.K_ESCAPE]:
        quit()

    # START SEARCH
    if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
        run_search(WIN, graph)
        graph.visualized = True

    # RELOAD SETTINGS
    if key_lock(keys, pygame.K_l, key_prev_states):
        pf.settings.load_from_json()

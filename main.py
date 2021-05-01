"""Pathfinder Visualizer Project"""
from typing import Sequence

import pygame

import pathfinder as pf
from pathfinder.maze import Maze
from pathfinder.node import Grid
from pathfinder.search import Algorithm
from pathfinder.utils import get_node_pos

# WINDOW SETUP
WIN = pygame.display.set_mode((pf.WIDTH, pf.HEIGHT))
pygame.display.set_caption(f"Pathfinder v{pf.version}")
pygame.display.set_icon(WIN)


def main():
    """Runs the pathfinder module"""

    def redraw_window(win):
        """Updates the entire screen"""
        WIN.fill(pf.LIGHT_BLUE)
        graph.draw_grid(win)
        pygame.display.update()

    def update_nodes():
        """Updates objects that have changed states"""
        pygame.display.update(Grid.cache)
        Grid.cache.clear()

    def run_search(win, graph_: Grid, auto=False):
        """
        Calls the Algorithm class to visualize
        the pathfinder algorithm using the Visualize class
        """
        if not graph_.has_bomb:
            node_list = [graph_.start, graph_.end]
            search_colors = [pf.BLUE]
        else:
            node_list = [graph_.start, graph_.bomb, graph_.end]
            search_colors = [pf.DARK_PINK, pf.BLUE]

        alg = Algorithm(pf.settings.default_alg, node_list, pf.GRID_OFFSET,
                        graph_.walls, graph_.weights)
        alg(win, graph_, search_colors, auto)

    def set_alg(keys: Sequence[bool], alg_map_: dict):
        """Sets the alg using keys and alg_map instead of multiple else ifs"""
        for key, new_alg in alg_map_.items():
            if keys[key] and keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                pf.settings.default_alg = new_alg
                graph.reset_visualization(WIN)
                graph.visualized = False
                break

    # SETUP VARIABLES
    graph = Grid(WIN)
    maze = Maze()
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
        click = pygame.mouse.get_pressed(num_buttons=3)
        keys = pygame.key.get_pressed()
        curr_node = get_node_pos(graph, mouse)
        set_alg(keys, alg_map)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        # DRAGGABLE NODES
        if curr_node in graph.draggable:
            if click[0]:
                dragging = True
                curr_node_temp = curr_node

        if not click[0]:
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
        if click[0] and not any(keys) and curr_node not in graph.draggable:
            graph.set_wall(WIN, curr_node)
            continue

        elif keys[pygame.K_b] and click[0] and not graph.has_bomb:
            graph.set_bomb(WIN, curr_node)

        elif keys[pygame.K_w] and click[0]:
            graph.set_weight(WIN, curr_node, pf.settings.default_alg)
            continue

        elif click[2] and curr_node not in (graph.end, graph.start):
            graph.clear_node(WIN, curr_node, True)

        # SET MAZES
        elif keys[pygame.K_m] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
            if pf.settings.default_alg in pf.WEIGHTED:
                maze.basic_weight_maze(WIN, graph)
                redraw_window(WIN)
                graph.visualized = False

        elif keys[pygame.K_m]:
            maze.basic_random_maze(WIN, graph)
            redraw_window(WIN)
            graph.visualized = False

        # RESET GRAPH
        elif keys[pygame.K_c]:
            graph.clear(WIN)
            graph.visualized = False

        # QUIT
        elif keys[pygame.K_ESCAPE]:
            return "quit"

        # START SEARCH
        if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
            print('Visualization started with:', pf.settings.default_alg.title())
            run_search(WIN, graph)
            graph.visualized = True
            print('Visualization done')

        # RELOAD SETTINGS
        if keys[pygame.K_l]:
            pf.settings.load_from_json()


if __name__ == '__main__':
    main()

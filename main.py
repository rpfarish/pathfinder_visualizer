"""Controls entire project"""
from typing import Sequence

import pygame

import pathfinder as pf
from pathfinder.maze import Maze
from pathfinder.node import Grid
from pathfinder.search import Algorithm
from pathfinder.utils import get_node_pos

WIN = pygame.display.set_mode((pf.WIDTH, pf.HEIGHT))
pygame.display.set_caption(f"Pathfinder v{pf.version}")
pygame.display.set_icon(WIN)


def main():
    """runs the pathfinder module"""

    def redraw_window(win):
        """updates the entire screen"""
        WIN.fill((175, 216, 248))
        graph.draw_grid(win)

        pygame.display.update()

    def update_nodes():
        """updates only objects that have changed states"""
        pygame.display.update(Grid.cache)
        Grid.cache.clear()

    clock = pygame.time.Clock()
    graph = Grid(WIN)
    graph.draw_grid(WIN)
    maze = Maze(pf.GRID_SIZE)
    curr_node_temp = None
    dragging = False

    WIN.fill((175, 216, 248))
    redraw_window(WIN)

    alg_map = {
        pygame.K_a: 'astar',
        pygame.K_b: 'bfs',
        pygame.K_f: 'dfs',
        pygame.K_d: 'dijkstra',
        pygame.K_g: 'greedy',
    }

    def run_search(win, graph_: Grid, auto=False):
        if not graph_.has_bomb:
            node_list = [graph_.start, graph_.end]
            search_colors = [pf.BLUE]
        else:
            node_list = [graph_.start, graph_.bomb, graph_.end]
            search_colors = [pf.DARK_PINK, pf.BLUE]

        alg = Algorithm(pf.settings.default_alg, node_list, pf.GRID_OFFSET,
                        graph_.walls, graph_.weights)
        alg(win, graph_, search_colors, auto)

    def set_alg(keys: Sequence[bool], alg_map: dict, was_visualized: bool):

        for key, new_alg in alg_map.items():
            alg_can_be_changed = keys[key] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT])
            if alg_can_be_changed:
                pf.settings.default_alg = new_alg
                was_visualized = False
                if new_alg in pf.settings.unweighted:
                    graph.clear_weights(WIN)

                for color in pf.SEARCH_COLORS:
                    graph.clear_searched(WIN, (color,))

                graph.clear_searched(WIN, (pf.YELLOW,))
                break

        return was_visualized

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        update_nodes()
        clock.tick(2000)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        curr_node = get_node_pos(graph, mouse)

        if click[0] and not any(keys):
            graph.set_wall(WIN, curr_node)
            continue

        elif keys[pygame.K_b] and click[0] and not graph.has_bomb:
            graph.set_bomb(WIN, curr_node)

        elif keys[pygame.K_w] and click[0]:
            graph.set_weight(WIN, curr_node, pf.settings.default_alg)
            continue

        elif click[2] and curr_node not in (graph.end, graph.start):
            graph.clear_node(WIN, curr_node, True)

        if curr_node in graph.draggable:
            if click[0]:
                dragging = True
                curr_node_temp = curr_node

        if dragging:
            if not click[0]:
                dragging = False

            elif curr_node_temp != curr_node:
                graph.set_drag_state(WIN, curr_node_temp, curr_node)
                curr_node_temp = curr_node

            if graph.visualized:
                run_search(WIN, graph, auto=True)

            continue

        graph.visualized = set_alg(keys, alg_map, graph.visualized)

        if keys[pygame.K_c]:
            graph.clear(WIN)
            graph.visualized = False

        elif keys[pygame.K_m] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
            if pf.settings.default_alg in pf.settings.weighted:
                maze.basic_weight_maze(WIN, graph)
                redraw_window(WIN)
                graph.visualized = False

        elif keys[pygame.K_m]:
            maze.basic_random_maze(WIN, graph)
            redraw_window(WIN)
            graph.visualized = False

        if keys[pygame.K_ESCAPE]:
            return "quit"

        if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
            print('Visualization started with:', pf.settings.default_alg.title())
            run_search(WIN, graph)
            print('Visualization done')
            graph.visualized = True


if __name__ == '__main__':
    main()

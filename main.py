"""Controls entire project"""

import pygame

import pathfinder as pf
from pathfinder.maze import Maze
from pathfinder.node import Grid
from pathfinder.search import Algorithm
from pathfinder.utils import get_node_pos

# - Pygame init -
WIN = pygame.display.set_mode((pf.WIDTH, pf.HEIGHT))
pygame.display.set_caption(f"Pathfinder v{pf.version}")
pygame.display.set_icon(WIN)


def main():
    """runs the pathfinder module"""

    # - Update display -
    def redraw_window(win):
        """updates the entire screen"""
        WIN.fill((175, 216, 248))
        graph.draw_grid(win)

        pygame.display.update()

    def update_nodes():
        """updates only objects that have changed states"""
        pygame.display.update(Grid.cache)
        Grid.cache.clear()

    # - Setup -
    clock = pygame.time.Clock()
    graph = Grid(WIN)
    graph.draw_grid(WIN)
    maze = Maze(pf.GRID_SIZE)
    alg_name = pf.settings.default_alg  # default alg
    curr_node_temp = None
    dragging = False
    visualized = False
    # fill and update the display
    WIN.fill((175, 216, 248))
    redraw_window(WIN)

    def run_search(win, graph_, auto=False):
        if not graph_.has_bomb:
            node_list = [graph_.start, graph_.end]
            search_colors = [pf.BLUE]
        else:
            node_list = [graph_.start, graph_.bomb, graph_.end]
            search_colors = [pf.DARK_PINK, pf.BLUE]

        alg = Algorithm(pf.settings.default_alg, node_list, pf.GRID_OFFSET,
                        graph_.walls, graph_.weights)
        alg(win, graph_, search_colors, auto)

    def set_alg(alg_):
        """resets weights if alg is switched to unweighted"""
        if alg_ not in pf.settings.weighted:
            graph.clear_weights(WIN)
            for color in pf.SEARCH_COLORS:
                graph.clear_searched(WIN, (color,))
            else:
                graph.clear_searched(WIN, (pf.YELLOW,))
        return alg_

    while True:

        # - Pygame events -
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        # - Update loop state -
        update_nodes()
        clock.tick(2000)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        curr_node = get_node_pos(graph, mouse)

        if curr_node in graph.draggable:
            if click[0]:
                dragging = True
                curr_node_temp = curr_node

        if dragging:
            if not click[0]:
                dragging = False
            if curr_node_temp != curr_node:
                graph.set_drag_state(WIN, curr_node_temp, curr_node)
                curr_node_temp = curr_node
                if visualized:
                    run_search(WIN, graph, auto=True)

            continue

        # - Set alg names -

        # A*
        if keys[pygame.K_a] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
            pf.settings.default_alg = set_alg('astar')

        # Dijkstra
        elif keys[pygame.K_d] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
            pf.settings.default_alg = set_alg('dijkstra')

        # BFS
        elif keys[pygame.K_b] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
            pf.settings.default_alg = set_alg('bfs')

        # DFS
        elif keys[pygame.K_f] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
            pf.settings.default_alg = set_alg('dfs')

        # Greedy
        elif keys[pygame.K_g] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
            pf.settings.default_alg = set_alg('greedy')

        # - Set node state -

        # Start
        elif keys[pygame.K_s] and click[0]:
            graph.set_start(WIN, curr_node)

        # End
        elif keys[pygame.K_e] and click[0]:
            graph.set_end(WIN, curr_node)

        # Bomb
        elif keys[pygame.K_b] and click[0]:
            graph.set_bomb(WIN, curr_node)
            # todo make bomb a png

        # Weight
        elif keys[pygame.K_w] and click[0]:
            graph.set_weight(WIN, curr_node, pf.settings.default_alg)

        # Wall
        elif click[0]:
            graph.set_wall(WIN, curr_node)

        # Reset
        elif click[2] and curr_node not in (graph.end, graph.start):
            graph.clear_node(WIN, curr_node, True)

        # Reset All Node
        elif keys[pygame.K_c]:
            visualized = False
            graph.clear(WIN)

        # - Mazes -

        # Basic weight maze
        elif keys[pygame.K_m] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
            if pf.settings.default_alg in pf.settings.weighted:
                visualized = False
                maze.basic_weight_maze(WIN, graph)
                redraw_window(WIN)

        # Basic random maze
        elif keys[pygame.K_m]:
            visualized = False
            maze.basic_random_maze(WIN, graph)
            redraw_window(WIN)

        # - Exit -
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            raise SystemExit

        # Start Visualization
        if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
            print('Visualization started with:', pf.settings.default_alg.title())
            # Start Search
            run_search(WIN, graph)
            visualized = True
            print('Visualization done')


if __name__ == '__main__':
    main()

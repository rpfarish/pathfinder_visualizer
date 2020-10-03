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
    # fill and update the display
    WIN.fill((175, 216, 248))
    redraw_window(WIN)

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
        node_indices = get_node_pos(graph, mouse)

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
            graph.set_start(WIN, node_indices)

        # End
        elif keys[pygame.K_e] and click[0]:
            graph.set_end(WIN, node_indices)

        # Bomb
        elif keys[pygame.K_b] and click[0]:
            graph.set_bomb(WIN, node_indices)
            # todo make bomb a png

        # Weight
        elif keys[pygame.K_w] and click[0]:
            graph.set_weight(WIN, node_indices, pf.settings.default_alg)

        # Wall
        elif click[0] and node_indices not in graph.draggable:
            graph.set_wall(WIN, node_indices)

        elif click[0] and node_indices in graph.draggable:
            print('trying to drag')

        # Reset
        elif click[2]:
            graph.clear_node(WIN, node_indices, True)

        # Reset All Node
        elif keys[pygame.K_c]:
            graph.clear(WIN)

        # - Mazes -

        # Basic weight maze
        elif keys[pygame.K_m] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
            if pf.settings.default_alg in pf.settings.weighted:
                maze.basic_weight_maze(WIN, graph)
                redraw_window(WIN)

        # Basic random maze
        elif keys[pygame.K_m]:
            maze.basic_random_maze(WIN, graph)
            redraw_window(WIN)

        # - Exit -
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            raise SystemExit

        # Start Visualization
        if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:

            if graph.start == (None, None) or graph.end == (None, None):
                print('Invalid start or end nodes')
                continue

            print('Visualization started with:', pf.settings.default_alg.title())

            if not graph.has_bomb:
                node_list = [graph.start, graph.end]
                search_colors = [pf.BLUE]
            else:
                node_list = [graph.start, graph.bomb, graph.end]
                search_colors = [pf.DARK_PINK, pf.BLUE]

            alg = Algorithm(pf.settings.default_alg, node_list, pf.GRID_OFFSET,
                            graph.walls, graph.weights)
            alg(WIN, graph, search_colors)

            print('Visualization done')


if __name__ == '__main__':
    main()

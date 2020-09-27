"""Controls entire project"""

import pygame

import pathfinder as pf
from pathfinder.maze import Maze
from pathfinder.node import Grid
from pathfinder.search import Algorithm
from pathfinder.utils import get_node_pos

version = '2.8.7'

# - Pygame init -
WIN = pygame.display.set_mode((pf.WIDTH, pf.HEIGHT))
pygame.display.set_caption(f"Pathfinder v{version}")
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
    maze = Maze(pf.grid_x, pf.grid_y)
    alg_name = 'astar'  # default alg
    # fill and update the display
    WIN.fill((175, 216, 248))
    redraw_window(WIN)

    def set_alg(alg_):
        """resets weights if alg is switched to unweighted"""
        if alg_ not in pf.weighted:
            graph.clear_weights(WIN)
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
            alg_name = set_alg('astar')

        # Dijkstra
        elif keys[pygame.K_d] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
            alg_name = set_alg('dijkstra')

        # BFS
        elif keys[pygame.K_b] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
            alg_name = set_alg('bfs')

        # DFS
        elif keys[pygame.K_f] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
            alg_name = set_alg('dfs')

        # Greedy
        elif keys[pygame.K_g] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
            alg_name = set_alg('greedy')

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
            graph.set_weight(WIN, node_indices, alg_name)

        # Wall
        elif click[0]:
            graph.set_wall(WIN, node_indices)

        # Reset
        elif click[2]:
            graph.clear_node(WIN, node_indices, True)

        # Reset All Node
        elif keys[pygame.K_c]:
            graph.clear(WIN)

        # - Mazes -

        # Basic weight maze
        elif keys[pygame.K_m] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
            if alg_name in pf.weighted:
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
            print('Visualization started with:', alg_name.title())

            if graph.has_bomb:
                node_list = [graph.start, graph.bomb, graph.end]

                alg = Algorithm(alg_name, node_list, graph.walls,
                                pf.grid_offset, graph.weights)

                alg.run_alg(WIN, graph, [pf.dark_pink, pf.blue])

            elif not graph.has_bomb:
                node_list = [graph.start, graph.end]

                alg = Algorithm(alg_name, node_list, graph.walls,
                                pf.grid_offset, graph.weights)

                alg.run_alg(WIN, graph, [pf.blue])

            print('Visualization done')


if __name__ == '__main__':
    main()

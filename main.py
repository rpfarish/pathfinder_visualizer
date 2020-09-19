"""Controls entire project"""
import pygame

from pathfinder.constants import HEIGHT, WIDTH, blue, dark_pink, grid_offset, \
    grid_x, grid_y
from pathfinder.maze import Maze
from pathfinder.node import Grid
from pathfinder.search.algorithm import Algorithm
from pathfinder.utils import get_node_pos

version = '2.8.1'

# - Pygame init -
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
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
    alg_name = 'dijkstra'  # default alg
    WIN.fill((175, 216, 248))
    redraw_window(WIN)

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
        if keys[pygame.K_a] and keys[pygame.K_LSHIFT]:
            alg_name = 'astar'

        # Dijkstra
        elif keys[pygame.K_d] and keys[pygame.K_LSHIFT]:
            alg_name = 'dijkstra'

        # BFS
        elif keys[pygame.K_b] and keys[pygame.K_LSHIFT]:
            alg_name = 'bfs'

        # DFS
        elif keys[pygame.K_f] and keys[pygame.K_LSHIFT]:
            alg_name = 'dfs'

        # Greedy
        elif keys[pygame.K_g] and keys[pygame.K_LSHIFT]:
            alg_name = 'greedy'

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

        # Basic random maze
        elif keys[pygame.K_m]:
            Maze(graph, grid_x, grid_y).basic_random_maze(WIN)
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
                                grid_offset, graph.weights)

                alg.run_alg(WIN, graph, [dark_pink, blue])

            elif not graph.has_bomb:
                node_list = [graph.start, graph.end]

                alg = Algorithm(alg_name, node_list, graph.walls,
                                grid_offset, graph.weights)

                alg.run_alg(WIN, graph, [blue])

            print('Visualization done')


if __name__ == '__main__':
    main()

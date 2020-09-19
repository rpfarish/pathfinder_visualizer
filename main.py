"""Controls entire project"""
import pygame

from pathfinder.constants import HEIGHT, WIDTH, blue, dark_pink, grid_offset, grid_x, grid_y
from pathfinder.node import Grid
from pathfinder.search.algorithm import Algorithm
from pathfinder.utils import foo_mystery, get_node_pos

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

version = '0.0.1'

pygame.display.set_caption(f"Pathfinder v{version}")

pygame.display.set_icon(WIN)


def main():
    """
    Runs the pathfinder module
    """
    run = True
    graph = Grid(WIN)
    graph.set_start(WIN, (int(grid_x * .25), grid_y // 2))
    graph.set_end(WIN, (int(grid_x * .75), grid_y // 2))
    clock = pygame.time.Clock()
    alg_name = 'astar'  # default alg

    def redraw_window(win):
        """Updates the entire screen"""
        WIN.fill((175, 216, 248))
        graph.draw_grid(win)
        pygame.display.update()

    def update_nodes():
        """Updates only objects that have changed states"""
        pygame.display.update(Grid.cache)
        Grid.cache.clear()

    WIN.fill((175, 216, 248))
    redraw_window(WIN)
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit

        update_nodes()
        clock.tick(2000)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()

        # Get the indices of what node the mouse is over
        node_indices = get_node_pos(graph, mouse)

        # Set alg name to A*
        if keys[pygame.K_a] and keys[pygame.K_LSHIFT]:
            alg_name = 'astar'

        # Set alg name to dijkstra
        elif keys[pygame.K_d] and keys[pygame.K_LSHIFT]:
            alg_name = 'dijkstra'

        # Set alg name to bfs
        elif keys[pygame.K_b] and keys[pygame.K_LSHIFT]:
            alg_name = 'bfs'

        # Set alg name to dfs
        elif keys[pygame.K_f] and keys[pygame.K_LSHIFT]:
            alg_name = 'dfs'

        # Set alg name to greedy
        elif keys[pygame.K_g] and keys[pygame.K_LSHIFT]:
            alg_name = 'greedy'

        # Set node to start
        elif keys[pygame.K_s] and click[0]:
            graph.set_start(WIN, node_indices)

        # Set node to end
        elif keys[pygame.K_e] and click[0]:
            graph.set_end(WIN, node_indices)

        # Set node to bomb
        elif keys[pygame.K_b] and click[0]:
            graph.set_bomb(WIN, node_indices)
            # todo make bomb a png

        # Set node to bomb
        elif keys[pygame.K_w] and click[0]:
            graph.set_weight(WIN, node_indices, alg_name)

        # Set node to wall
        elif click[0]:
            graph.set_wall(WIN, node_indices)

        # Reset node
        elif click[2]:
            graph.clear_node(WIN, node_indices, True)

        # Reset all nodes
        if keys[pygame.K_c]:
            graph.clear(WIN)

        # Allow the user to do something good with their life
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            raise SystemExit

        # Start Visualization
        if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
            print('Visualization started')

            if graph.has_bomb:
                node_list = [graph.start, graph.bomb, graph.end]
                alg = Algorithm(alg_name, node_list, graph.walls, grid_offset, graph.weights)
                alg.run_alg(WIN, graph, [dark_pink, blue])
            else:
                node_list = [graph.start, graph.end]
                alg = Algorithm(alg_name, node_list, graph.walls, grid_offset, graph.weights)
                alg.run_alg(WIN, graph, [blue])

            print('visualization done')

        # todo setup ui
        # todo setup menus
        # todo setup tutorial
        # todo give user the ability to lock or to be able to draw over the start and end
        # todo toggle the cost of each node
        # todo make search speed a slider


if __name__ == '__main__':
    main()

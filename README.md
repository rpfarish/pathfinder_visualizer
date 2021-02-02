# Pathfinding Visualizer

Welcome to the Pathfinding Visualizer! I was always fascinated by optimization problems
and pathfinding algorithms are all about finding the optimal solution as quickly and efficiently as possible.
This pathfinder was made with pygame and uses various search algorithms to find the target node in a undirected graph.
Made with python 3.9 and pygame 2.0.0. 

## Meet the Algorithms

This application supports the following algorithms: 

- **Dijkstra's Algorithm** (weighted): The famous Dijkstra's Algorithm invented by Edsger Dijkstra and
    implemented with a priority queue; guarantees the shortest path

- **A*** **Search** (weighted):  A* achieves better performance than Dijkstra by using a heuristic to inform the path search; guarantees the shortest path

- **Greedy Best-First Search** (weighted): a faster version of A* and uses the heuristic more liberally to inform the path search; does not guarantee the shortest path

- **Breadth-First Search** (unweighted): a great overall algorithm; guarantees the shortest path

- **Depth-First Search** (unweighted): elegant in some situations, but it is not an efficient algorithm at all for pathfinding; does not guarantee the shortest path.


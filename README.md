# Pathfinding Visualizer

Welcome to the Pathfinding Visualizer! I was always fascinated by optimization problems
and pathfinding algorithms are all about finding the optimal solution as quickly and efficently as possible.
This pathfinder was made with pygame and uses various search algorithms to find the end node in a undirected graph.

## Meet the Algorithms

This application supports the following algorithms: 

- **Dijkstra's Algorithm** (weighted): the grandfather of pathfinding algorithms; guarantees the shortest path

- **A*** **Search** (weighted): probably the best pathfinding algorithm; uses a heuristic to inform the path search; guarantees the shortest path

- **Greedy Best-First Search** (weighted): a faster version of A* and uses a heuristic more liberally to inform the path search; does not guarantee the shortest path

- **Breadth-First Search** (unweighted): a great overall algorithm; guarantees the shortest path

- **Depth-First Search** (unweighted): not an efficient algorithm at all and does not find the shortest path.

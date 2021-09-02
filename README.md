# Pathfinding Visualizer

Welcome to the Pathfinding Visualizer! I have always been fascinated by optimization problems and pathfinding algorithms
are all about finding the optimal solution as quickly and efficiently as possible. Pathfinder uses various search
algorithms to find the target node in an undirected graph which may have obstacles (edge cuts). Made with Python 3.9 and
Pygame 2.0.0.

## Meet the Algorithms

Pathfinder supports the following algorithms:

- **Dijkstra's Algorithm** (weighted): The father of pathfinding algorithms; implemented with a priority queue and
  guarantees the shortest path.

- **A*** **Search** (weighted):  A* uses heuristics to guarantee the shortest path much faster than Dijkstra's
  Algorithm; arguably the best algorithm.

- **Greedy Best-first Search** (weighted): A faster, more heuristic-heavy version of A*; does not guarantee the shortest
  path.

- **Breadth-first Search** (unweighted): A great overall algorithm; guarantees the shortest path.

- **Depth-first Search** (unweighted): Elegant in some situations, however for pathfinding, it is not an efficient
  algorithm at all; does not guarantee the shortest path.

## How to Install

You can install all required packages with pip by using the Terminal or Command Prompt. Download the code or use Git to
clone the repo, and then navigate into the project directory using the Terminal. Type the
command `pip install -r requirements.txt` (`pip3` on Unix). This should install the required packages to run the
program. Run `main.py` to run the program. Note: This current version only supports `pygame 2.0.0` and any other version
is not guaranteed to work.

## Keyboard and Mouse Commands

- **Visualize Algorithm:** <kbd>Spacebar</kbd> **or** <kbd>Enter</kbd>
- **Place Wall:** <kbd>Left Click</kbd>
- **Clear Node:** <kbd>Right Click</kbd>
- **Clear/Reset Grid:** <kbd>C</kbd>
- **Pause/Resume Search:** <kbd>P</kbd>
- **Exit Search:** <kbd>Backspace</kbd>
- **Place Weight:**  <kbd>W</kbd> + <kbd>Left Click</kbd> **(only for weighted algs)**
- **Place Bomb:** <kbd>B</kbd> + <kbd>Left Click</kbd>  **(at most 1 Bomb)**
- **Generate Random Maze:** <kbd>M</kbd>
- **Generate Random Weight Maze:** <kbd>Shift</kbd> + <kbd>M</kbd> **(only for weighted algs)**
- **Reload Settings:** <kbd>L</kbd> **(from settings.json)**
- **Quit:** <kbd>Esc</kbd>

### Switch the current algorithm:

- **A*** **:** <kbd>Shift</kbd> + <kbd>A</kbd>
- **Greedy:** <kbd>Shift</kbd> + <kbd>G</kbd>
- **Dijkstra:** <kbd>Shift</kbd> + <kbd>D</kbd>
- **BFS:** <kbd>Shift</kbd> + <kbd>B</kbd>
- **DFS:** <kbd>Shift</kbd> + <kbd>F</kbd>

### Draggable Nodes:

The **start** (green), **end** (red) and **bomb** (pink) nodes are all draggable. Just **left click** and drag to
reposition. After the algorithm has been visualized, dragging a node will recalculate and re-visualize the optimal path
in real time
(optimal path not guaranteed for Greedy or DFS).

### Mazes:

The random maze generator features the ability to recursively generate a maze which always has a solution.

## Settings

| Setting | Description |
| --- | --- |
| `default_alg`| Default algorithm loaded. This is the same as the last used algorithm. Default value is `dijkstra`.|
| `dark_mode`  | Enable/disable dark mode. This functionality darkens the grid to dark gray. Default value is `true` (enabled).|
| `screen_size`| Default window width and height. For full-screen, change to your monitor's dimensions. |
| `grid_size`  | Width and Height values determine the size of the grid. Default values are `"WIDTH": 50, "HEIGHT": 25`. |
| `node_size`  | The width and height of a given node. Default value is `25`.| 
| `path_speed` | The number of milliseconds between each path node being drawn. Default value is `0.07`.|
| `search_speed`| The number of milliseconds between each node being visualized during the search area being drawn. Default value is `0.02`. |
| `weight_density` | The number of equivalent nodes required to pass through a weight node. Default value is `10`.|
| `maze_density_percentage` | The probability that a given node will have a wall placed on it when a maze is generated. If the percentage is too high, it will result in a recursion error. Default value is `0.33`.|
| `enable_diagonals` | When `true` pathfinder visualizer will use diagonals to find an optimal path. Default value is `false` (not enabled). |
| `visualize_when_dragging` | When `true` pathfinder visualizer will redraw the search area and the path when dragging any node. Default value is `true` (enabled). |

### Editing Settings:

`settings.json` is the file that stores all the user changeable settings. Some settings may require a restart before
taking effect.

For some more fun, try editing the following settings:

```json
{
  "grid_size": {
    "WIDTH": 90,
    "HEIGHT": 45
  },
  "node_size": 12
}
```

If the visualization is too slow, decrease the `search_speed` setting.

```json
{
  "grid_size": {
    "WIDTH": 169,
    "HEIGHT": 85
  },
  "node_size": 6,
  "path_speed": 0.05,
  "search_speed": 0
}
```

## License

This program is licensed under the [MIT License](https://github.com/rpfarish/pathfinder_visualizer/blob/master/LICENSE).
# Pathfinding Visualizer

Welcome to the Pathfinding Visualizer! I was always fascinated by optimization problems and pathfinding algorithms are
all about finding the optimal solution as quickly and efficiently as possible. This pathfinder was made with pygame and
uses various search algorithms to find the target node in a undirected graph. Made with python 3.9 and pygame 2.0.0.

## Meet the Algorithms

This application supports the following algorithms:

- **Dijkstra's Algorithm** (weighted): The famous Dijkstra's Algorithm invented by Edsger Dijkstra and implemented with
  a priority queue; guarantees the shortest path

- **A*** **Search** (weighted):  A* achieves better performance than Dijkstra by using a heuristic to inform the path
  search; guarantees the shortest path

- **Greedy Best-First Search** (weighted): a faster version of A* and uses the heuristic more liberally to inform the
  path search; does not guarantee the shortest path

- **Breadth-First Search** (unweighted): a great overall algorithm; guarantees the shortest path

- **Depth-First Search** (unweighted): elegant in some situations, but it is not an efficient algorithm at all for
  pathfinding; does not guarantee the shortest path.

## How to Install

You can install all required packages with pip by using the terminal or command prompt. Download the Code or use Git to
clone the repo and then navigate into the project directory on the terminal. Type the
command `pip install -r requirements.txt` (`pip3` on Unix). This should install the required packages to run the
program. Run `main.py` to run the program. Note: This current version only supports `pygame 2.0.0` and any other version
of pygame is not guaranteed to work.

## Keyboard and Mouse Commands

- **Visualize Algorithm:** <kbd>Spacebar</kbd> **or** <kbd>Enter</kbd>
- **Place Wall:** <kbd>Left Click</kbd>
- **Clear Node:** <kbd>Right Click</kbd>
- **Reset Grid:** <kbd>C</kbd>
- **Pause Search:** <kbd>P</kbd>
- **Exit Search:** <kbd>Backspace</kbd>
- **Place Weight:**  <kbd>W</kbd> + <kbd>Left Click</kbd>
- **Place Bomb:** <kbd>B</kbd> + <kbd>Left Click</kbd>  **(at most 1)**
- **Generate Random Maze:** <kbd>M</kbd>
- **Generate Random Weight Maze:** <kbd>Shift</kbd> + <kbd>M</kbd>
- **Reload Settings:** <kbd>L</kbd>
- **Quit:** <kbd>Esc</kbd>

### Switch the current algorithm:

- **A***: <kbd>Shift</kbd> + <kbd>A</kbd>
- **Greedy:** <kbd>Shift</kbd> + <kbd>G</kbd>
- **Dijkstra:** <kbd>Shift</kbd> + <kbd>D</kbd>
- **BFS:** <kbd>Shift</kbd> + <kbd>B</kbd>
- **DFS:** <kbd>Shift</kbd> + <kbd>F</kbd>

### Draggable Nodes:

The `start` (green), `end` (red) and `bomb` (pink) nodes are all draggable. Just click and drag to reposition.

## Options

| Option | Description |
| --- | --- |
| `dark_mode`  | Enable/disable dark mode. This functionality darkens the grid to dark gray. Default value is `true`.|
| `grid_size` |  Width and Height values determine the size of the grid. Default values are `"WIDTH": 50, "HEIGHT": 25`. |
| `node_size` |  The width and height of a given node. Default value is `25`.| 
| `default_alg`| Default algorithm loaded. This is the same as the last used algorithm. Default value is `"dijkstra"`. |
| `screen_size`| Default window width and height. For full-screen, change to your monitor's dimensions. |
| `search_speed` | The number of milliseconds between each node being visualized during the search area being drawn. Default value is `0.0055`. |
| `path_speed` | The number of milliseconds between each node being visualized during the path being drawn. Default value is `0.07`.|
| `weight_density` | The number of equivalent nodes required to pass through a weight node. Default value is `10`.|
| `maze_density` | The percentage of walls put down for a maze. Higher percentages result a denser maze.|
| `enable_diagonals` | When `true` pathfinder visualizer will use diagonals to find an optimal path. Default value is `false`. |
| `visualize_when_dragging` | When `true` pathfinder visualizer will redraw the search area and the path when dragging any node. Default value is `true`. |

### Editing Settings:

The `settings.json` is the file that stores all the user changeable settings. Some settings may require a restart before
taking effect.

For some more fun, try the following settings:

```json
{
  "grid_size": {
    "WIDTH": 90,
    "HEIGHT": 45
  },
  "node_size": 12
}
```

## License

This program is licensed under the [MIT License](https://github.com/rpfarish/pathfinder_visualizer/blob/master/LICENSE).
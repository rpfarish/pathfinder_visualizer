"""Default settings backup in the case of settings.json getting deleted"""

default_settings_backup = {
    "file": "settings.json",
    "version": "3.1.4",
    "default_alg": "astar",
    "dark_mode": True,
    "screen_size": {
        "WIDTH": 1355,
        "HEIGHT": 680
    },
    "grid_size": {
        "WIDTH": 50,
        "HEIGHT": 25
    },
    "node_size": 25,
    "path_speed": 0.07,
    "search_speed": 0.002,
    "weight_density": 10,
    "maze_density_percentage": 0.33,
    "enable_diagonals": False,
    "visualize_when_dragging": True
}

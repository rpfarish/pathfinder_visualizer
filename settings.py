import json

default = {
    "default_alg": "astar",
    "search_speed": 0.0055,
    "weight_density": 15,
    "weighted": [
        "astar",
        "dijkstra",
        "greedy"
    ],
    "node_size": [
        25,
        25
    ],
    "screen_size": {
        "WIDTH": 1400,
        "HEIGHT": 700
    },
    "grid_size": {
        "WIDTH": 50,
        "HEIGHT": 25
    },
    "version": "2.9.2"
}


class Settings:
    """Loads settings from a .json file"""

    def __init__(self, file):
        self.file = file
        self.version = None
        self.weighted = None
        self.grid_size = None
        self.node_size = None
        self.default_alg = None
        self.screen_size = None
        self.search_speed = None
        self.weight_density = None
        self.load()

    def load(self):
        """Open and save attributes from a .json file"""
        with open(self.file) as file:
            settings = json.loads(file.read())

        for setting in settings.items():
            setattr(self, *setting)

        # self.save()

    def save(self):
        with SaveFile(self.file) as file:
            file.write(json.dumps(self.__dict__))

    # todo implement save method that takes current attributes and writes them to the json file


class SaveFile:
    def __init__(self, file):
        self.file = file
        self.file_obj = None

    def __enter__(self):
        self.file_obj = open(self.file, "w")
        return self.file_obj

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None or exc_val is not None:
            print("Error:", exc_type, exc_val, exc_tb)
            self.file_obj.write(json.dumps(default))
        self.file_obj.close()
        return True

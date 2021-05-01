"""Loads and Saves Settings"""
import json

from .default_settings import default_settings_backup


class Settings:
    """Loads settings from a .json file"""
    done_loading = False

    def __init__(self, file):
        self.file = file
        self.version = None
        self.dark_mode = None
        self.grid_size = None
        self.node_size = None
        self.default_alg = None
        self.path_speed = None
        self.screen_size = None
        self.search_speed = None
        self.maze_density = None
        self.weight_density = None
        self.enable_diagonals = None
        self.visualize_when_dragging = None

        self.load_from_json()

    def __setattr__(self, key, value):
        """Inspect setter for tracking the attributes accessed."""
        super().__setattr__(key, value)
        if self.__class__.done_loading:
            self.save_to_json()

    def load_from_json(self):
        """Open and save attributes from a .json file"""
        self.__class__.done_loading = False
        print("Loading Settings")
        with SaveFile(self.file) as file:
            settings = json.loads(file.read())

        for setting in settings.items():
            setattr(self, *setting)
        else:
            self.__class__.done_loading = True

    def save_to_json(self):
        """Gets class attributes and dumps to .json file"""
        with SaveFile(self.file, "w") as file:
            file.write(json.dumps(self.__dict__))


class SaveFile:
    """
    Context Manager to save files and if there were any errors
    loads and saves default settings
    """

    def __init__(self, file, mode="r"):
        self.file = file
        self.mode = mode
        self.file_obj = None

    def __enter__(self):
        self.file_obj = open(self.file, self.mode)
        return self.file_obj

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None or exc_val is not None:
            print("Error:", exc_type, exc_val, exc_tb)
            self.file_obj.close()
            self.file_obj = open(self.file, "w")
            self.file_obj.write(json.dumps(default_settings_backup))
        self.file_obj.close()
        return True

"""Pathfinder is a set of Python modules designed for visualizing paths between two points"""
import pygame

try:
    from pathfinder.constants import *
except (ImportError, IOError) as e:
    quit(code=f"Pathfinder.constants cannot be imported.\nError message: {e}")

__version__ = settings.version
compatible_pygame_version = '2.1.0'

if str(pygame.version.vernum) == compatible_pygame_version:
    print(f'Pathfinder {__version__} (Pygame {pygame.version.vernum})')
else:
    error = f"Installed Pygame version {pygame.version.vernum} is incompatible with the current version " \
            f"of Pathfinder {__version__} \nPlease use the commands 'pip uninstall pygame' " \
            f"and 'pip install pygame=={compatible_pygame_version}' to install the correct version of pygame."
    quit(code=error)

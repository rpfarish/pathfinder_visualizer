"""Pathfinder is a set of Python modules designed for visualizing paths between two points"""
import pygame

try:
    from pathfinder.constants import *
except (ImportError, IOError):
    quit(code="Pathfinder.constants is missing")

__version__ = settings.version

if str(pygame.version.vernum) == '2.0.0':
    print(f'Pathfinder {__version__} (Pygame {pygame.version.vernum})')

else:
    error = f"Installed Pygame version {pygame.version.vernum} is incompatible with the current version" \
            f"of Pathfinder {__version__} \nPlease use the commands 'pip uninstall pygame' " \
            f"and 'pip install pygame==2.0.0' to install the correct version of pygame."
    quit(code=error)

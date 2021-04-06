# """Pathfinder is a set of Python modules designed for visualizing paths between two points"""

try:
    from pathfinder.constants import *
except (ImportError, IOError):
    quit(code="Pathfinder.constants is missing")

# try:
#     import pathfinder.utils
# except (ImportError, IOError):
#     quit(code="Pathfinder.utils is missing")
#
# print('Pathfinder Instantiated')

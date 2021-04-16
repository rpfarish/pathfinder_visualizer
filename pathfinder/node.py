"""Creates and controls the getting setting of Node objects"""

import pygame

from . import settings
from .constants import DARK_BLUE, GREEN, GRID_X, GRID_Y, HEIGHT, OFFSET, ORANGE, PINK, RED, SEARCH_COLORS, SPACESHIP, \
    WHITE, YELLOW, node_size, weight_density


class Grid:
    """
    Creates arrays of node objects and allows accessing them
    through a dict graph structure with coordinates as keys.
    Accessing the graph structure or grid can be done through
    using self as the dict object itself.
    """
    cache = []

    def __init__(self, win):
        self.grid = {(x, y): Node(win, WHITE, x, y, node_size, node_size)
                     for y in range(GRID_Y) for x in range(GRID_X)}

        self.has_bomb = False
        self.bomb = (None, None)
        self.visualized = False

        # set start and end to the first and third quartiles
        self.start = (int(GRID_X * .25), GRID_Y // 2)
        self.end = (int(GRID_X * .75), GRID_Y // 2)
        self[self.start].make_start()
        self[self.end].make_end()

        self.wall_color = DARK_BLUE
        self.weight_color = ORANGE
        self.clear_color = WHITE

    def __getitem__(self, key):
        return self.grid[key]

    def __setitem__(self, key, value):
        self.grid[key] = value

    def __iter__(self):
        return iter(self.grid)

    def __len__(self):
        return len(self.grid)

    @property
    def walls(self):
        """:returns list of all walls as a int tuple"""
        return [pos for pos in self if self[pos].color == self.wall_color]

    @property
    def weights(self):
        """:returns dict of all weights as a int tuple: int map"""
        return {pos: weight_density if self[pos].color == self.weight_color
        else 1 for pos in self}

    @property
    def draggable(self):
        """:returns dict of draggable nodes"""
        dragging = {
            self.start: self[self.start],
            self.end: self[self.end],
        }
        if self.has_bomb:
            dragging[self.bomb] = self[self.bomb]
        return dragging

    def values(self):
        """:returns iterator of grid values"""
        return iter(self.grid.values())

    def items(self):
        """:returns iterator of grid items"""
        return iter(self.grid.items())

    def keys(self):
        """:returns iterator of grid keys"""
        return iter(self.grid.keys())

    def draw_grid(self, win):
        """draws all nodes"""
        for node in self.values():
            node.draw(win)

    def draw_node(self, win, node: tuple[int, int], redraw=True):
        """draws the node then caches its rect object to draw later"""
        self[node].draw(win, redraw=redraw)

    def set_start(self, win, node: tuple[int, int]):
        """sets the state of the node to start"""
        if node != self.end and node != self.bomb:
            self.start = node
            self[node].make_start()
            self.draw_node(win, node)

    def set_end(self, win, node: tuple[int, int]):
        """sets the state of the node to end"""
        if node != self.start and node != self.bomb:
            self.end = node
            self[node].make_end()
            self.draw_node(win, node)

    def set_bomb(self, win, node):
        """sets the state of the node to bomb"""
        if not self.has_bomb:
            self.visualized = False
        if node != self.start and node != self.end:
            self.has_bomb = True
            self.bomb = node
            self[node].make_bomb()
            self.draw_node(win, node)

    def set_wall(self, win, node: tuple[int, int]):
        """sets the state of the node to wall"""
        if node != self.start and node != self.end:
            self.clear_node(win, node)
            self[node].make_wall()
            self.draw_node(win, node)

    def set_weight(self, win, node: tuple[int, int], alg: str):
        """sets the state of the node to weight"""
        if alg in settings.weighted and node != self.start and node != self.end:
            self.clear_node(win, node)
            self[node].make_weight()
            self.draw_node(win, node)

    def set_drag_state(self, win, last, curr):
        """
        Sets the state of the nodes when it is
        being dragged and dragged over
        """
        if last == curr:
            return
        self[curr].set_prev_state()

        if self[last].color == GREEN:
            self.set_start(win, curr)
        elif self[last].color == RED:
            self.set_end(win, curr)
        elif self[last].color == PINK:
            self.set_bomb(win, curr)

        self[last].prev_state()
        self[last].draw(win)

    def clear_walls(self, win):
        """resets all wall nodes"""
        for pos, node in self.items():
            if node.color == DARK_BLUE:
                node.clear()
                self.draw_node(win, pos)

    def clear_weights(self, win):
        """resets all weight nodes"""
        for pos, node in self.items():
            if node.color == ORANGE:
                node.clear()
                self.draw_node(win, pos)

    def clear_node(self, win, node: tuple[int, int], draw=False):
        """resets the state of the node based on its current color"""
        if self[node].color == PINK:
            self.has_bomb = False
            self.bomb = (None, None)

        self[node].clear()
        self.draw_node(win, node, redraw=draw)

    def clear(self, win, reset_targets=True):
        """
        Resets all nodes in grid by calling clear_node
        on every object in grid.
        """
        start = self.start
        end = self.end
        bomb = self.bomb
        for node in self:
            if self[node].color != WHITE:
                self.clear_node(win, node, True)
        if reset_targets:
            self.set_start(win, (int(GRID_X * .25), GRID_Y // 2))
            self.set_end(win, (int(GRID_X * .75), GRID_Y // 2))
            self.has_bomb = False
            self.bomb = (None, None)
        else:
            self.set_start(win, start)
            self.set_end(win, end)
            if None not in bomb:
                self.set_bomb(win, bomb)

    def clear_searched(self, win, color, update=True):
        """
        resets all nodes that are in color
        :param update: if update, the whole display updates
        :param win: pygame surface
        :param color: tuple of colors
        """
        for node in self.values():
            if node.color in color:
                node.clear()
                node.draw(win)
        if update:
            pygame.display.update()

    def reset_visualization(self, win):
        """Clears all nodes"""

        if settings.default_alg not in settings.weighted:
            self.clear_weights(win)

        for color in SEARCH_COLORS:
            self.clear_searched(win, (color,))

        self.clear_searched(win, (YELLOW,))


class Node:
    """
    The class to set states,
    draws and get states for each node in the grid.
    """
    _offset = 1

    def __init__(self, win, color, x, y, width, height,
                 x_coord=None, y_coord=None):

        self.win = win
        self.color = color
        self.x = HEIGHT // GRID_Y * x + OFFSET if x_coord is None else x_coord
        self.y = HEIGHT // GRID_Y * y + OFFSET if y_coord is None else y_coord
        self.x_coord = x
        self.y_coord = y
        self.width = width + Node._offset
        self.height = height + Node._offset
        self.rect_obj = pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.height)
        )
        self.is_target = False
        self.prev_state = self.clear

    def __eq__(self, other):
        if not isinstance(self, type(self)) or type(self) is not type(other):
            return False

        elif len(self.__dict__) != len(other.__dict__):
            return False

        elif self.x == other.x and self.y == other.y and self.width == other.width \
                and self.height == other.height and self.color == other.color \
                and self.x_coord == other.x_coord and self.y_coord == other.y_coord \
                and self.is_target == other.is_target:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return f'{self.__class__.__name__}({self.win}, {self.color}, {self.x_coord}, ' \
               f'{self.y_coord}, {self.width - self.__class__._offset}, ' \
               f'{self.height - self.__class__._offset})'

    def __str__(self):
        return f'class name: {self.__class__.__name__},  color: {self.color}, ' \
               f'x coord: {self.x_coord}, y coord: {self.y_coord}, ' \
               f'width: {self.width}, height: {self.height}, x pos: {self.x}, y pos: {self.y})'

    def draw(self, win, redraw=False):
        """
        Draws the rect and updates the rectangle object to
        update one obj at a time instead of the whole screen.
        """

        self.rect_obj = pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.height)
        )
        if redraw:
            Grid.cache.append(self.rect_obj)

        if self.is_target:
            win.blit(SPACESHIP, (self.x, self.y))

    def make_wall(self):
        """sets a node to the wall color"""
        self.color = DARK_BLUE

    def make_start(self):
        """sets a node to the start color"""
        self.color = GREEN

    def make_end(self):
        """sets a node to the end color"""
        self.color = RED

    def make_bomb(self):
        """sets a node to the bomb color"""
        self.color = PINK

    def make_weight(self):
        """sets a node to the weight color"""
        self.color = ORANGE

    def clear(self):
        """sets the node to its original color"""
        self.color = WHITE
        self.prev_state = self.clear

    def set_prev_state(self):
        """
        Sets the previous state of the node
        by color to a first-class function
        """
        if self.color == DARK_BLUE:
            self.prev_state = self.make_wall
        elif self.color == ORANGE:
            self.prev_state = self.make_weight
        elif self.color == WHITE:
            self.prev_state = self.clear
        elif self.color == GREEN:
            self.prev_state = self.make_start
        elif self.color == RED:
            self.prev_state = self.make_end

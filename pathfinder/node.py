"""Creates and controls the getting setting of Node objects"""

import pygame

from .constants import HEIGHT, OFFSET, black, green, grid_x, grid_y, node_size, orange, pink, red, spaceship, \
    weighted, white

TARGET = spaceship


class Grid:
    """Creates arrays of node objects"""
    cache = []

    def __init__(self, win):
        self.grid = {(x, y): Node(win, white, x, y, node_size[0], node_size[1])
                     for y in range(grid_y) for x in range(grid_x)}

        self.has_start = self.has_end = True
        self.has_bomb = False

        # set start and end to the first and third quartiles
        self.start = (int(grid_x * .25), grid_y // 2)
        self.end = (int(grid_x * .75), grid_y // 2)
        self.grid[self.start].make_start()
        self.grid[self.end].make_end()

        self.bomb = (None, None)
        # todo visualized does nothing
        self.visualized = False
        self.weight = 10

    def draw_grid(self, win):
        """draws all nodes"""
        for node in self.grid.values():
            node.draw(win)

    def set_start(self, win, node):
        """sets the state of the node to start"""
        if not self.has_start and node != self.end and node != self.bomb:
            self.has_start = True
            self.start = node
            self.grid[node].make_start()
            self.draw_node(win, node)

    def set_end(self, win, node):
        """sets the state of the node to end"""
        if not self.has_end and node != self.start and node != self.bomb:
            self.has_end = True
            self.end = node
            self.grid[node].make_end()
            self.draw_node(win, node)

    def set_bomb(self, win, node):
        """sets the state of the node to bomb"""
        if not self.has_bomb and node != self.start and node != self.end:
            self.has_bomb = True
            self.bomb = node
            self.grid[node].make_bomb()
            self.draw_node(win, node)

    def set_wall(self, win, node):
        """sets the state of the node to wall"""
        self.clear_node(win, node)
        self.grid[node].make_wall()
        self.draw_node(win, node)

    def set_weight(self, win, node, alg):
        """sets the state of the node to weight"""

        if alg in weighted:
            self.clear_node(win, node)
            self.grid[node].make_weight()
            self.draw_node(win, node)

    def clear_walls(self, win):
        """resets all wall nodes"""
        for node in self.walls:
            self.grid[node].clear()
            self.draw_node(win, node)

    def clear_weights(self, win):
        """resets all weights nodes"""
        for node in self.grid:
            if self.grid[node].color == orange:
                self.grid[node].clear()
                self.draw_node(win, node)

    def clear_node(self, win, node, draw=False):
        """resets the state of the node based on its current color"""
        if self.grid[node].color == green:
            self.has_start = False
            self.start = (None, None)
        elif self.grid[node].color == red:
            self.has_end = False
            self.end = (None, None)
        elif self.grid[node].color == pink:
            self.has_bomb = False
            self.bomb = (None, None)
        # Set color to white
        self.grid[node].clear()

        if draw:
            self.draw_node(win, node)

    def clear(self, win, reset_targets=True):
        """
        Resets all nodes in grid by calling clear_node
        on every object in grid.
        """
        start = self.start
        end = self.end
        bomb = self.bomb
        for node in self.grid:
            if self.grid[node].color != white:
                self.clear_node(win, node, True)
        if reset_targets:
            self.set_start(win, (int(grid_x * .25), grid_y // 2))
            self.set_end(win, (int(grid_x * .75), grid_y // 2))
            self.has_bomb = False
            self.bomb = (None, None)
        else:
            self.set_start(win, start)
            self.set_end(win, end)
            if bomb != (None, None):
                self.set_bomb(win, bomb)

    def draw_node(self, win, node):
        """draws the node then caches its rect object to draw later"""
        self.grid[node].draw(win)
        Grid.cache.append(self.grid[node].rect_obj)

    def draw(self, win, node):
        """draws the node"""
        self.grid[node].draw(win)

    @property
    def walls(self):
        """:returns list of all walls as a int tuple"""
        return [(self.grid[pos].get_pos())
                for pos in self.grid if self.grid[pos].color == black]

    @property
    def weights(self):
        """:returns list of all walls as a int tuple"""
        return {(self.grid[pos].get_pos()): 10
        if self.grid[pos].color == orange else 1 for pos in self.grid}

    @property
    def draggable(self):
        """:returns dict of draggable nodes"""
        return {
            self.start: self.grid[self.start],
            self.end: self.grid[self.end],
            self.bomb: self.grid[self.bomb]
        }

    def clear_searched(self, win, color):
        """
        resets all nodes that are in color
        :param win: pygame surface
        :param color: tuple of colors
        """
        for node in self.grid.values():
            if node.color in color:
                node.clear()
                node.draw(win)
        else:
            pygame.display.update()


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
        self.x = HEIGHT // grid_y * x + OFFSET if x_coord is None else x_coord
        self.y = HEIGHT // grid_y * y + OFFSET if y_coord is None else y_coord
        self.x_coord = x
        self.y_coord = y
        self.width = width + Node._offset
        self.height = height + Node._offset
        self.rect_obj = pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.height)
        )
        self.dragging = False
        self.is_target = False

    def __eq__(self, other):
        if not isinstance(self, type(self)) or type(self) is not type(other):
            return False

        if len(self.__dict__) != len(other.__dict__):
            return False

        if self.x == other.x and self.y == other.y and self.width == other.width and self.height == other.height \
                and self.color == other.color and self.x_coord == other.y_coord and self.x_coord == other.y_coord \
                and self.dragging == other.dragging and self.is_target == other.is_target:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return f'{self.__class__.__name__}({self.win}, {self.color}, {self.x_coord}, ' \
               f'{self.y_coord}, {self.width - self.__class__._offset}, {self.height - self.__class__._offset})'

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
            win.blit(TARGET, (self.x, self.y))

    # def update_obj(self, win):
    #     self.rect_obj = pygame.draw.rect(
    #         win, self.color, (self.x, self.y, self.width, self.height)
    #     )

    #
    # def resize(self, win, size):
    #     temp = self.rect_obj.center
    #     self.width += size[0]
    #     self.height += size[1]
    #     self.update_obj(win)
    #
    #     cool = temp
    #     px, py = self.rect_obj.center
    #     cx, cy = cool
    #
    #     temp = px - cx, py - cy
    #
    #     self.x -= temp[0]
    #     self.y -= temp[1]

    def hover(self, mouse) -> bool:
        """:return True if mouse is inside the rectangle else False"""
        x_pos, y_pos = mouse
        if self.x - OFFSET < x_pos < self.x + self.width + OFFSET and \
                self.y - OFFSET < y_pos < self.y + self.height + OFFSET:
            return True
        else:
            return False

    def make_wall(self):
        """sets a node to the wall color"""
        self.color = black

    def make_start(self):
        """sets a node to the start color"""
        self.color = green

    def make_end(self):
        """sets a node to the end color"""
        self.color = red

    def make_bomb(self):
        """sets a node to the bomb color"""
        self.color = pink

    def make_weight(self):
        """sets a node to the weight color"""
        self.color = orange

    def clear(self):
        """sets the node to its original color"""
        self.color = white

    def get_pos(self):
        """:returns tuple of the xy coordinate of the current node"""
        return self.x_coord, self.y_coord

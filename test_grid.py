"""Tests Grid class"""
import unittest
from collections.abc import Iterable

import pygame

import pathfinder as pf
from pathfinder.node import Grid

WIN = pygame.display.set_mode((1, 1))


# todo check all return values

class TestGrid(unittest.TestCase):

    def setUp(self) -> None:
        """Sets up Grid instances for every test"""
        self.graph = Grid(WIN)
        self.graph2 = Grid(WIN)

    def tearDown(self):
        """Tears down Grid instances for every test"""
        Grid.cache.clear()

    def test_walls(self):
        # assert Expected, Actual
        walls = self.graph.walls
        self.assertIsInstance(walls, list)
        self.assertEqual(0, len(walls))

        for wall, node in zip(walls, self.graph.grid):
            if self.graph[wall].color == self.graph.clear_color == node.color:
                pass
            else:
                self.assertEqual(self.graph[wall].color, self.graph.clear_color)
                self.assertEqual(self.graph.clear_color, node.color)

        for node in self.graph.grid.values():
            node.color = self.graph.wall_color

        walls = self.graph.walls
        self.assertEqual(len(self.graph.grid), len(walls))

    def test_weights(self):
        # assert Expected, Actual
        self.assertIsInstance(self.graph.weights, dict)
        for (pos, weight), node in zip(self.graph.weights.items(), self.graph.grid):
            self.assertEqual(1, weight)
            self.assertEqual(pos, node)
        for node in self.graph.grid:
            self.graph.grid[node].color = pf.ORANGE
            self.assertEqual(10, self.graph.weights[node])

    def test_draggable(self):
        # assert Expected, Actual
        drag = self.graph.draggable
        self.assertIn(self.graph.start, drag, 'The start node is not in draggable')
        self.assertIn(self.graph.end, drag, 'The end node is not in draggable')
        self.assertNotIn(self.graph.bomb, drag, 'The bomb node is in draggable')
        self.assertIn(None, self.graph.bomb, 'The bomb node is not None')
        self.assertFalse(self.graph.has_bomb, 'graph.has_bomb is True')

        self.assertIs(drag[self.graph.start], self.graph.grid[self.graph.start],
                      'The start node obj is not in draggable')
        self.assertIs(drag[self.graph.end], self.graph.grid[self.graph.end], 'The end node obj is not in draggable')

        self.graph.has_bomb = True
        self.graph.bomb = (1, 1)

        drag = self.graph.draggable

        self.assertIn(self.graph.start, drag, 'The start node is not in draggable')
        self.assertIn(self.graph.end, drag, 'The end node is not in draggable')
        self.assertIn(self.graph.bomb, drag, 'The bomb node is not in draggable')
        self.assertNotIn(None, self.graph.bomb, 'The bomb node is None')
        self.assertTrue(self.graph.has_bomb, 'graph.has_bomb is False')

        self.assertIs(drag[self.graph.start], self.graph.grid[self.graph.start],
                      'The start node obj is not in draggable')
        self.assertIs(drag[self.graph.end], self.graph.grid[self.graph.end], 'The end node obj is not in draggable')
        self.assertIs(drag[self.graph.bomb], self.graph.grid[self.graph.bomb], 'The end node obj is not in draggable')

    def test_values(self):
        self.assertIsInstance(self.graph.values(), Iterable, 'values does not return an iterable')
        for node1, node2 in zip(self.graph.grid.values(), self.graph.values()):
            self.assertIs(node1, node2, f'the two nodes {node1} and {node2} are not the same Object')

    def test_items(self):
        self.assertIsInstance(self.graph.items(), Iterable, 'items does not return an iterable')
        for (node1, obj1), (node2, obj2) in zip(self.graph.grid.items(), self.graph.items()):
            self.assertIs(node1, node2, f'the two nodes {node1} and {node2} are not the same Object')
            self.assertIs(obj1, obj2, f'the two Objs {obj1} and {obj2} are not the same Object')

    def test_keys(self):
        self.assertIsInstance(self.graph.keys(), Iterable, 'keys does not return an iterable')
        for node1, node2 in zip(self.graph.grid.keys(), self.graph.keys()):
            self.assertIs(node1, node2, f'the two nodes {node1} and {node2} are not the same Object')

    def test_draw_grid(self):
        self.graph.draw_grid(WIN)
        for node, node2 in zip(self.graph.grid.values(), self.graph2.grid.values()):
            self.assertEqual(node, node2, f'Nodes 1 and 2 are not equal to each other')
            self.assertNotIn(node.rect_obj, Grid.cache, 'The rect object was appended to the Grid cache')
            self.assertFalse(node.is_target, 'The node.is_target is True')

    def test_draw_node(self):
        self.assertEqual(self.graph.grid[(0, 0)], self.graph2.grid[(0, 0)],
                         'The nodes (0, 0) from graph and graph2 are not equal')
        self.assertNotIn(self.graph.grid[(0, 0)].rect_obj, Grid.cache, 'The rect object was appended to the Grid cache')

        self.graph.draw_node(WIN, (0, 0))
        self.assertEqual(self.graph.grid[(0, 0)], self.graph2.grid[(0, 0)],
                         'The nodes (0, 0) from graph and graph2 are not equal')
        self.assertIn(self.graph.grid[(0, 0)].rect_obj, Grid.cache,
                      'The rect object was not appended to the Grid cache')
        node = Grid.cache.pop()
        self.assertIs(node, self.graph.grid[(0, 0)].rect_obj,
                      'The node popped from the cache is not the same obj as the node.rect_obj')
        self.assertFalse(self.graph.grid[(0, 0)].is_target, 'The node.is_target was True')

    def test_set_start(self):
        self.assertNotIn(None, self.graph.start)
        self.assertNotIn(None, self.graph.end)
        self.assertIn(None, self.graph.bomb)

        node1 = (0, 0)
        node2 = (1, 1)
        set_start = self.graph.set_start

        # check that start is not set if the node to be set is either the end or the bomb
        self.graph.bomb = self.graph.end = node1

        self.assertIsNone(set_start(WIN, node1))
        self.assertNotEqual(self.graph.start, node1)
        self.assertNotEqual(self.graph[node1].color, pf.GREEN)

        self.graph.end = node2
        self.graph.bomb = self.graph.end = node1
        self.graph.bomb = node2

        self.assertIsNone(set_start(WIN, node1))
        self.assertNotEqual(self.graph.start, node1)
        self.assertNotEqual(self.graph[node1].color, pf.GREEN)

        self.assertNotIn(None, self.graph.start)
        self.assertNotIn(None, self.graph.end)
        self.assertNotIn(None, self.graph.bomb)

        # check if the start is set then the correct node is set
        self.graph.bomb = node2
        self.graph.end = (2, 2)
        self.assertIsNone(self.graph.set_start(WIN, node1))
        self.assertTupleEqual(node1, self.graph.start)
        self.assertTupleEqual(self.graph[node1].color, pf.GREEN)

        self.assertNotIn(None, self.graph.start)
        self.assertNotIn(None, self.graph.end)
        self.assertNotIn(None, self.graph.bomb)

        self.graph.bomb = self.graph.end = (2, 2)
        self.assertIsNone(self.graph.set_start(WIN, node1))
        self.assertTupleEqual(node1, self.graph.start)
        self.assertTupleEqual(self.graph[node1].color, pf.GREEN)

        self.assertNotIn(None, self.graph.start)
        self.assertNotIn(None, self.graph.end)
        self.assertNotIn(None, self.graph.bomb)

    def test_set_end(self):
        self.assertNotIn(None, self.graph.start)
        self.assertNotIn(None, self.graph.end)
        self.assertIn(None, self.graph.bomb)

        node1 = (0, 0)
        node2 = (1, 1)
        set_end = self.graph.set_end

        # check that end is not set if the node to be set is either the start or the bomb
        self.graph.bomb = self.graph.start = node1

        self.assertIsNone(set_end(WIN, node1))
        self.assertNotEqual(self.graph.end, node1)
        self.assertNotEqual(self.graph[node1].color, pf.RED)

        self.graph.start = node2
        self.graph.bomb = self.graph.start = node1
        self.graph.bomb = node2

        self.assertIsNone(set_end(WIN, node1))
        self.assertNotEqual(self.graph.end, node1)
        self.assertNotEqual(self.graph[node1].color, pf.RED)

        self.assertNotIn(None, self.graph.start)
        self.assertNotIn(None, self.graph.end)
        self.assertNotIn(None, self.graph.bomb)

        # check if the end is set then the correct node is set
        self.graph.bomb = node2
        self.graph.start = (2, 2)
        self.assertIsNone(self.graph.set_end(WIN, node1))
        self.assertTupleEqual(node1, self.graph.end)
        self.assertTupleEqual(self.graph[node1].color, pf.RED)

        self.assertNotIn(None, self.graph.start)
        self.assertNotIn(None, self.graph.end)
        self.assertNotIn(None, self.graph.bomb)

        self.graph.bomb = self.graph.start = (2, 2)
        self.assertIsNone(self.graph.set_end(WIN, node1))
        self.assertTupleEqual(node1, self.graph.end)
        self.assertTupleEqual(self.graph[node1].color, pf.RED)

        self.assertNotIn(None, self.graph.start)
        self.assertNotIn(None, self.graph.end)
        self.assertNotIn(None, self.graph.bomb)

    def test_set_bomb(self):
        self.assertNotIn(None, self.graph.start)
        self.assertNotIn(None, self.graph.end)
        self.assertIn(None, self.graph.bomb)

        node = (0, 0)
        node2 = (1, 1)
        node3 = (2, 2)

        self.graph.start = self.graph.end = node
        self.assertIsNone(self.graph.set_bomb(WIN, node))
        self.assertTupleEqual(self.graph.bomb, self.graph2.bomb)
        self.assertFalse(self.graph.has_bomb)

        self.assertIn(None, self.graph.bomb)

        self.graph.end = node2
        self.assertIsNone(self.graph.set_bomb(WIN, node))
        self.assertTupleEqual(self.graph.bomb, self.graph2.bomb)
        self.assertIn(None, self.graph.bomb)
        self.assertFalse(self.graph.has_bomb)

        self.graph.start = self.graph.end = node

        self.graph.end = node2
        self.assertIsNone(self.graph.set_bomb(WIN, node))
        self.assertTupleEqual(self.graph.bomb, self.graph2.bomb)
        self.assertIn(None, self.graph.bomb)
        self.assertFalse(self.graph.has_bomb)

        self.graph.start = node2
        self.graph.end = node3

        self.assertIsNone(self.graph.set_bomb(WIN, node))
        self.assertTupleEqual(node, self.graph.bomb)
        self.assertNotIn(None, self.graph.bomb)
        self.assertTupleEqual(self.graph[node].color, pf.PINK)
        self.assertTrue(self.graph.has_bomb)

    def test_set_wall(self):
        node = (0, 0)
        node2 = (1, 1)
        node3 = (2, 2)

        self.graph.start = self.graph.end = node
        self.assertIsNone(self.graph.set_wall(WIN, node))
        self.assertTupleEqual(self.graph[node].color, self.graph2[node].color)

        self.graph.start = node2

        self.graph.start = self.graph.end = node
        self.assertIsNone(self.graph.set_wall(WIN, node))
        self.assertTupleEqual(self.graph[node].color, self.graph2[node].color)

        self.graph.start = self.graph.end = node
        self.graph.start = node3

        self.graph.start = self.graph.end = node

        self.assertIsNone(self.graph.set_wall(WIN, node))
        self.assertTupleEqual(self.graph[node].color, self.graph2[node].color)

        self.graph.start = self.graph.end = node2

        self.assertIsNone(self.graph.set_wall(WIN, node))
        self.assertTupleEqual(self.graph[node].color, pf.DARK_BLUE)

    def test_set_weight(self):
        node = (0, 0)
        node2 = (1, 1)
        node3 = (2, 2)
        weighted = 'astar'
        unweighted = 'bfs'

        # checking with unweighted
        self.graph.start = self.graph.end = node
        self.assertIsNone(self.graph.set_weight(WIN, node, unweighted))
        self.assertTupleEqual(self.graph[node].color, self.graph2[node].color)

        self.graph.start = self.graph.end = node
        self.graph.start = node2
        self.assertIsNone(self.graph.set_weight(WIN, node, unweighted))
        self.assertTupleEqual(self.graph[node].color, self.graph2[node].color)

        self.graph.start = self.graph.end = node
        self.graph.end = node2
        self.assertIsNone(self.graph.set_weight(WIN, node, unweighted))
        self.assertTupleEqual(self.graph[node].color, self.graph2[node].color)

        self.graph.start = self.graph.end = node
        self.graph.start = node3
        self.assertIsNone(self.graph.set_weight(WIN, node, unweighted))
        self.assertTupleEqual(self.graph[node].color, self.graph2[node].color)

        self.graph.start = self.graph.end = node
        self.graph.end = node3
        self.assertIsNone(self.graph.set_weight(WIN, node, unweighted))
        self.assertTupleEqual(self.graph[node].color, self.graph2[node].color)

        self.graph.start = self.graph.end = node2
        self.assertIsNone(self.graph.set_weight(WIN, node, unweighted))
        self.assertTupleEqual(self.graph[node].color, self.graph2[node].color)

        # checking with weighted
        self.graph.start = self.graph.end = node
        self.assertIsNone(self.graph.set_weight(WIN, node, weighted))
        self.assertTupleEqual(self.graph[node].color, self.graph2[node].color)

        self.graph.start = self.graph.end = node
        self.graph.start = node2
        self.assertIsNone(self.graph.set_weight(WIN, node, weighted))
        self.assertTupleEqual(self.graph[node].color, self.graph2[node].color)

        self.graph.start = self.graph.end = node
        self.graph.end = node2
        self.assertIsNone(self.graph.set_weight(WIN, node, weighted))
        self.assertTupleEqual(self.graph[node].color, self.graph2[node].color)

        self.graph.start = self.graph.end = node
        self.graph.start = node3
        self.assertIsNone(self.graph.set_weight(WIN, node, weighted))
        self.assertTupleEqual(self.graph[node].color, self.graph2[node].color)

        self.graph.start = self.graph.end = node
        self.graph.end = node3
        self.assertIsNone(self.graph.set_weight(WIN, node, weighted))
        self.assertTupleEqual(self.graph[node].color, self.graph2[node].color)

        self.graph.start = self.graph.end = node2
        self.assertIsNone(self.graph.set_weight(WIN, node, weighted))
        self.assertTupleEqual(self.graph[node].color, pf.ORANGE)


if __name__ == '__main__':
    unittest.main()

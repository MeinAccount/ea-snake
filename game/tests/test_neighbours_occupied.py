import unittest

from game.direction import Directions


class TestNeighboursOccupied(unittest.TestCase):
    def test_single(self):
        positions = [(20, 20)]
        self.assertEqual(Directions.neighbours_occupied(Directions.RIGHT, positions), [False, False, False])
        self.assertEqual(Directions.neighbours_occupied(Directions.UP, positions), [False, False, False])
        self.assertEqual(Directions.neighbours_occupied(Directions.LEFT, positions), [False, False, False])
        self.assertEqual(Directions.neighbours_occupied(Directions.DOWN, positions), [False, False, False])

    def test_simple(self):
        positions = [(20, 20), (19, 20)]
        self.assertEqual(Directions.neighbours_occupied(Directions.RIGHT, positions), [False, False, False])
        self.assertEqual(Directions.neighbours_occupied(Directions.UP, positions), [True, False, False])
        self.assertEqual(Directions.neighbours_occupied(Directions.LEFT, positions), [False, True, False])
        self.assertEqual(Directions.neighbours_occupied(Directions.DOWN, positions), [False, False, True])

    def test_line(self):
        positions = [(18, 19), (18, 18), (19, 18), (20, 18), (20, 19), (20, 20), (19, 20), (18, 20), (17, 20), (16, 20), (15, 20), (14, 20)]
        self.assertEqual(Directions.neighbours_occupied(Directions.RIGHT, positions), [True, False, True])
        self.assertEqual(Directions.neighbours_occupied(Directions.UP, positions), [False, True, False])
        self.assertEqual(Directions.neighbours_occupied(Directions.LEFT, positions), [True, False, True])
        self.assertEqual(Directions.neighbours_occupied(Directions.DOWN, positions), [False, True, False])

    def test_edges(self):
        pass

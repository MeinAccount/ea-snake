import unittest

from game.direction import Board, Directions, GRID_WIDTH, GRID_HEIGHT


class TestNeighboursFree(unittest.TestCase):
    def test_single(self):
        positions = [(20, 20)]
        self.assertEqual(Board.neighbours_free(Directions.RIGHT, positions), [True, True, True])
        self.assertEqual(Board.neighbours_free(Directions.UP, positions), [True, True, True])
        self.assertEqual(Board.neighbours_free(Directions.LEFT, positions), [True, True, True])
        self.assertEqual(Board.neighbours_free(Directions.DOWN, positions), [True, True, True])

    def test_simple(self):
        positions = [(20, 20), (19, 20)]
        self.assertEqual(Board.neighbours_free(Directions.RIGHT, positions), [True, True, True])
        self.assertEqual(Board.neighbours_free(Directions.UP, positions), [False, True, True])
        self.assertEqual(Board.neighbours_free(Directions.LEFT, positions), [True, False, True])
        self.assertEqual(Board.neighbours_free(Directions.DOWN, positions), [True, True, False])

    def test_line(self):
        positions = [(18, 19), (18, 18), (19, 18), (20, 18), (20, 19), (20, 20), (19, 20), (18, 20), (17, 20), (16, 20),
                     (15, 20), (14, 20)]
        self.assertEqual(Board.neighbours_free(Directions.RIGHT, positions), [False, True, False])
        self.assertEqual(Board.neighbours_free(Directions.UP, positions), [True, False, True])
        self.assertEqual(Board.neighbours_free(Directions.LEFT, positions), [False, True, False])
        self.assertEqual(Board.neighbours_free(Directions.DOWN, positions), [True, False, True])

    def test_edges(self):
        top_left = [(0, 0)]
        self.assertEqual(Board.neighbours_free(Directions.RIGHT, top_left), [False, True, True])
        self.assertEqual(Board.neighbours_free(Directions.UP, top_left), [False, False, True])
        self.assertEqual(Board.neighbours_free(Directions.LEFT, top_left), [True, False, False])
        self.assertEqual(Board.neighbours_free(Directions.DOWN, top_left), [True, True, False])

        bottom_right = [(GRID_WIDTH - 1, GRID_HEIGHT - 1)]
        self.assertEqual(Board.neighbours_free(Directions.RIGHT, bottom_right), [True, False, False])
        self.assertEqual(Board.neighbours_free(Directions.UP, bottom_right), [True, True, False])
        self.assertEqual(Board.neighbours_free(Directions.LEFT, bottom_right), [False, True, True])
        self.assertEqual(Board.neighbours_free(Directions.DOWN, bottom_right), [False, False, True])

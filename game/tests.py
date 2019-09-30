import unittest

from game.direction import compute_normalized_angle, Directions


class TestNormalizedAngle(unittest.TestCase):
    def test_right(self):
        # right
        self.assertEqual(compute_normalized_angle(Directions.RIGHT, (0, 0), (1, 0)), 0)

        # up
        self.assertEqual(compute_normalized_angle(Directions.RIGHT, (0, 0), (0, -1)), 0.5)

        # down
        self.assertEqual(compute_normalized_angle(Directions.RIGHT, (0, 0), (0, 1)), -0.5)

        # right-up
        self.assertEqual(compute_normalized_angle(Directions.RIGHT, (0, 0), (1, -1)), 0.25)

        # right-down
        self.assertEqual(compute_normalized_angle(Directions.RIGHT, (0, 0), (1, 1)), -0.25)

        # left-up
        self.assertEqual(compute_normalized_angle(Directions.RIGHT, (0, 0), (-1, -1)), 0.75)

        # left-down
        self.assertEqual(compute_normalized_angle(Directions.RIGHT, (0, 0), (-1, 1)), -0.75)

    def test_up(self):
        # up
        self.assertEqual(compute_normalized_angle(Directions.UP, (0, 0), (0, -1)), 0)

        # left
        self.assertEqual(compute_normalized_angle(Directions.UP, (0, 0), (-1, 0)), 0.5)

        # right
        self.assertEqual(compute_normalized_angle(Directions.UP, (0, 0), (1, 0)), -0.5)

        # up-left
        self.assertEqual(compute_normalized_angle(Directions.UP, (0, 0), (-1, -1)), 0.25)

        # up-right
        self.assertEqual(compute_normalized_angle(Directions.UP, (0, 0), (1, -1)), -0.25)

        # down-left
        self.assertEqual(compute_normalized_angle(Directions.UP, (0, 0), (-1, 1)), 0.75)

        # down-right
        self.assertEqual(compute_normalized_angle(Directions.UP, (0, 0), (1, 1)), -0.75)

    def test_left(self):
        # left
        self.assertEqual(compute_normalized_angle(Directions.LEFT, (0, 0), (-1, 0)), 0)

        # up
        self.assertEqual(compute_normalized_angle(Directions.LEFT, (0, 0), (0, -1)), -0.5)

        # down
        self.assertEqual(compute_normalized_angle(Directions.LEFT, (0, 0), (0, 1)), 0.5)

        # left-up
        self.assertEqual(compute_normalized_angle(Directions.LEFT, (0, 0), (-1, -1)), -0.25)

        # left-down
        self.assertEqual(compute_normalized_angle(Directions.LEFT, (0, 0), (-1, 1)), 0.25)

        # right-up
        self.assertEqual(compute_normalized_angle(Directions.LEFT, (0, 0), (1, -1)), -0.75)

        # right-down
        self.assertEqual(compute_normalized_angle(Directions.LEFT, (0, 0), (1, 1)), 0.75)

    def test_down(self):
        # down
        self.assertEqual(compute_normalized_angle(Directions.DOWN, (0, 0), (0, 1)), 0)

        # left
        self.assertEqual(compute_normalized_angle(Directions.DOWN, (0, 0), (-1, 0)), -0.5)

        # right
        self.assertEqual(compute_normalized_angle(Directions.DOWN, (0, 0), (1, 0)), 0.5)

        # down-left
        self.assertEqual(compute_normalized_angle(Directions.DOWN, (0, 0), (-1, 1)), -0.25)

        # down-right
        self.assertEqual(compute_normalized_angle(Directions.DOWN, (0, 0), (1, 1)), 0.25)

        # up-left
        self.assertEqual(compute_normalized_angle(Directions.DOWN, (0, 0), (-1, -1)), -0.75)

        # up-right
        self.assertEqual(compute_normalized_angle(Directions.DOWN, (0, 0), (1, -1)), 0.75)


if __name__ == '__main__':
    unittest.main()

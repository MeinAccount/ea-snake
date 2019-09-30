import math
from typing import Tuple, List


class Directions:
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3

    @staticmethod
    def to_left(direction) -> int:
        return (direction + 1) % 4

    @staticmethod
    def to_right(direction) -> int:
        return (direction - 1) % 4

    @staticmethod
    def apply(direction, pos):
        (x, y) = pos
        if direction == Directions.RIGHT:
            return x + 1, y
        if direction == Directions.UP:
            return x, y - 1
        if direction == Directions.LEFT:
            return x - 1, y
        if direction == Directions.DOWN:
            return x, y + 1

    @staticmethod
    def neighbours_occupied(direction, positions) -> List[bool]:
        occupied = [False, False, False]
        neighbours = [Directions.apply(Directions.to_left(direction), positions[0]),
                      Directions.apply(direction, positions[0]),
                      Directions.apply(Directions.to_right(direction), positions[0])]
        for pos in positions:
            for i in range(0, 3):
                if pos == neighbours[i]:
                    occupied[i] = True

        # TODO: handle edges

        return occupied


def compute_normalized_angle(direction: int, snake: Tuple[int, int], apple: Tuple[int, int]) -> float:
    """ Computes the angle to the apple
        The angle is relative to the current movement direction and normalized to [-1, 1]
    """
    # compute atan2 with apple rotated around snake for down direction
    if direction == Directions.RIGHT:
        angle = math.atan2(-(apple[1] - snake[1]), apple[0] - snake[0])
    elif direction == Directions.UP:
        angle = math.atan2(-(apple[0] - snake[0]), -(apple[1] - snake[1]))
    elif direction == Directions.LEFT:
        angle = math.atan2(apple[1] - snake[1], -(apple[0] - snake[0]))
    elif direction == Directions.DOWN:
        angle = math.atan2(apple[0] - snake[0], apple[1] - snake[1])

    return angle / math.pi

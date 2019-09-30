import math
from typing import Tuple


class Directions:
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3


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


def direction_apply(direction, pos):
    (x, y) = pos
    if direction == Directions.RIGHT:
        return x + 1, y
    if direction == Directions.UP:
        return x, y - 1
    if direction == Directions.LEFT:
        return x - 1, y
    if direction == Directions.DOWN:
        return x, y + 1

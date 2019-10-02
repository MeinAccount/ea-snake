import math
from typing import Tuple, List

GRID_WIDTH = 50
GRID_HEIGHT = 50


class Directions:
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3

    @staticmethod
    def to_left(direction: int) -> int:
        return (direction + 1) % 4

    @staticmethod
    def to_right(direction: int) -> int:
        return (direction - 1) % 4

    @staticmethod
    def apply(direction: int, pos: Tuple[int, int]):
        (x, y) = pos
        if direction == Directions.RIGHT:
            return x + 1, y
        if direction == Directions.UP:
            return x, y - 1
        if direction == Directions.LEFT:
            return x - 1, y
        if direction == Directions.DOWN:
            return x, y + 1


class Board:
    @staticmethod
    def neighbours_free(direction: int, positions: List[Tuple[int, int]]) -> Tuple[List[bool], float, float, float]:
        """
        :param direction: direction to check
        :param positions: list of positions - with list head assumed as head
        :return: list of three bools: [left is free, forward is free, right is free]
        """
        free = [True, True, True]
        neighbours = [Directions.apply(Directions.to_left(direction), positions[0]),
                      Directions.apply(direction, positions[0]),
                      Directions.apply(Directions.to_right(direction), positions[0])]

        # for computing distance in each direction
        left_max = up_max = 0
        right_min = GRID_WIDTH
        down_min = GRID_HEIGHT

        # check if neighbour is one of the positions
        pos_iter = iter(positions)
        next(pos_iter)  # skip first
        for pos in pos_iter:
            if pos[1] == positions[0][1]:  # shared y coordinate
                if pos[0] <= positions[0][0]:  # to left
                    left_max = max(left_max, pos[0])
                else:  # to right
                    right_min = min(right_min, pos[0])
            elif pos[0] == positions[0][0]:  # shared x coordinate
                if pos[1] <= positions[0][1]:  # above
                    up_max = max(up_max, pos[1])
                else:  # to right
                    down_min = min(down_min, pos[1])

            # check if is neighbour
            # TODO: this could be merged with above if
            for i in range(0, 3):
                if pos == neighbours[i]:
                    free[i] = False

        # handle edges
        for i in range(0, 3):
            if neighbours[i][0] == -1 or neighbours[i][0] == GRID_WIDTH or \
                    neighbours[i][1] == -1 or neighbours[i][1] == GRID_HEIGHT:
                free[i] = False

        # compute relative distance to neighbours
        neighbour_direction_to_distance = {
            Directions.apply(Directions.RIGHT, positions[0]): right_min - positions[0][0],
            Directions.apply(Directions.UP, positions[0]): positions[0][1] - up_max,
            Directions.apply(Directions.LEFT, positions[0]): positions[0][0] - left_max,
            Directions.apply(Directions.DOWN, positions[0]): down_min - positions[0][1],
        }

        return free, neighbour_direction_to_distance[neighbours[0]], neighbour_direction_to_distance[neighbours[1]], \
               neighbour_direction_to_distance[neighbours[2]]

    @staticmethod
    def compute_normalized_angle(direction: int, snake: Tuple[int, int], apple: Tuple[int, int]) -> float:
        """ Computes the angle to the apple
            The angle is relative to the current movement direction and normalized to [-1, 1]
        """
        # compute atan2 with apple rotated around snake for down direction
        if direction == Directions.RIGHT:
            angle = math.atan2(snake[1] - apple[1], apple[0] - snake[0])
        elif direction == Directions.UP:
            angle = math.atan2(snake[0] - apple[0], snake[1] - apple[1])
        elif direction == Directions.LEFT:
            angle = math.atan2(apple[1] - snake[1], snake[0] - apple[0])
        elif direction == Directions.DOWN:
            angle = math.atan2(apple[0] - snake[0], apple[1] - snake[1])

        return angle / math.pi

import math
from typing import Callable, Tuple

import numpy as np

from ea.dnn import chromo_predict
from game.direction import Board
from game.state import GameState


def dnn_to_handler(chromo: Tuple[np.ndarray, np.ndarray]) -> Callable[[GameState], int]:
    def dnn_handler(state: GameState) -> int:
        angle = Board.compute_normalized_angle(state.direction, state.positions[0], state.apple_pos)
        param = Board.neighbours_free(state.direction, state.positions)

        action = chromo_predict(chromo, angle, *param)
        return (state.direction + action) % 4

    return dnn_handler


def av_score(step_handler: Callable[[GameState], int], amount: int) -> float:
    score = []
    for i in range(amount):
        score.append(compute_score(step_handler))
    return sum(score) / len(score)


def compute_score(step_handler: Callable[[GameState], int]) -> float:
    state = GameState((20, 20))

    step_count = 0
    reward = 0
    distance_to_apple = state.distance_to_apple()

    while step_count <= distance_to_apple * 2 * math.sqrt(state.length):
        state.direction = step_handler(state)
        step_count += 1

        self_intersecting, has_grown = state.move()
        if not self_intersecting:
            return reward
        elif has_grown:
            reward += distance_to_apple / math.sqrt(step_count) * math.sqrt(state.length)

            step_count = 0
            distance_to_apple = state.distance_to_apple()

    return reward

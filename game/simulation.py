from typing import Callable, Tuple

import numpy as np

from ea.dnn import chromo_predict
from game.direction import Board
from game.state import GameState





def dnn_to_handler(chromo: Tuple[np.ndarray, np.ndarray]) -> Callable[[GameState], int]:
    def dnn_handler(state: GameState) -> int:
        angle = Board.compute_normalized_angle(state.direction, state.positions[0], state.apple_pos)
        neighbours_free = Board.neighbours_free(state.direction, state.positions)

        action = chromo_predict(chromo, angle, neighbours_free)
        return (state.direction + action) % 4

    return dnn_handler


def av_score(step_handler: Callable[[GameState], int], amount: int, top_score_factor) -> Tuple[float, int]:
    score = []
    for i in range(amount):
        score.append(compute_score(step_handler, top_score_factor))
    return update_top_score_factor(sum(score)/len(score), top_score_factor)


def compute_score(step_handler: Callable[[GameState], int], top_score_factor) -> float:
    state = GameState((20, 20))
    step_count = 0
    while step_count <= top_score_factor * 120:
        state.direction = step_handler(state)
        step_count += 1
        if not state.move():
            return state.length
    return state.length


def update_top_score_factor(score, top_score_factor):
    if score > top_score_factor:
        top_score_factor = score
        print("Best: {}".format(top_score_factor))
    return score, top_score_factor

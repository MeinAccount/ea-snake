from typing import Callable

from ea.dnn import chromo_predict
from game.direction import Board
from game.state import GameState


def dnn_to_handler(chromo) -> Callable[[GameState], int]:
    def dnn_handler(state: GameState) -> int:
        angle = Board.compute_normalized_angle(state.direction, state.positions[0], state.apple_pos)
        neighbours_free = Board.neighbours_free(state.direction, state.positions)

        action = chromo_predict(chromo, angle, neighbours_free)
        return (state.direction + action) % 4

    return dnn_handler


def compute_score(step_handler: Callable[[GameState], int]) -> float:
    state = GameState((20, 20))
    # reward = 0
    step_count = 0
    while step_count <= 1000:
        state.direction = step_handler(state)
        if not state.move():
            return state.length

        # reward += state.length
        step_count += 1

    return state.length

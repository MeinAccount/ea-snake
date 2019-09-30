from typing import Callable

from game.direction import Board
from game.state import GameState
from render import SimpleHandler


def compute_with_dnn(model) -> float:
    def dnn_handler(state: GameState) -> int:
        angle = Board.compute_normalized_angle(state.direction, state.positions[0], state.apple_pos)
        neighbours_free = Board.neighbours_free(state.direction, state.positions)

        # TODO: compute score based on angle and neighbours_free
        pass

    return compute_score(dnn_handler)


def compute_score(step_handler: Callable[[GameState], int]) -> float:
    state = GameState((20, 20))
    reward = 0
    step_count = 0
    while step_count <= 1000:
        state.direction = step_handler(state)
        if not state.move():
            return reward

        reward += state.length
        step_count += 1

    return reward


if __name__ == '__main__':
    print(compute_score(SimpleHandler().handle))

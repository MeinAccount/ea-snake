from typing import Callable

from game.data import Snake, Apple
from game.direction import Board
from render import SimpleHandler


def dnn_to_handler(model) -> Callable[[Snake, Apple], int]:
    def dnn_handler(snake: Snake, apple: Apple) -> int:
        angle = Board.compute_normalized_angle(snake.current_direction, snake.pos[0], apple.pos)
        neighbours_free = Board.neighbours_free(snake.current_direction, snake.pos)

        # TODO: compute score based on angle and neighbours_free
        pass

    return dnn_handler


def compute_score(step_handler: Callable[[Snake, Apple], int]) -> int:
    snake = Snake((20, 20))
    apple = Apple()

    reward = 0
    step_count = 0
    while step_count <= 1000:
        snake.current_direction = step_handler(snake, apple)
        if not snake.move(apple):
            return reward

        reward += snake.length
        step_count += 1

    return reward


if __name__ == '__main__':
    print(compute_score(SimpleHandler().handle))

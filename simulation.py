from typing import Callable

from data import Snake, Apple


def compute_score(step_handler: Callable[[Snake, Apple], int]) -> int:
    snake = Snake((20, 20))
    apple = Apple()

    reward = 0
    while True:
        snake.current_direction = step_handler(snake, apple)
        if not snake.move(apple):
            return reward

        reward += snake.length

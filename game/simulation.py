from typing import Callable

from game.data import Snake, Apple
from render import SimpleHandler


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

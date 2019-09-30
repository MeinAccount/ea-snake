import math
from typing import Callable

from game.data import Snake, Apple
from render import SimpleHandler


def dnn_to_handler(model) -> Callable[[Snake, Apple], int]:
    def dnn_handler(snake: Snake, apple: Apple) -> int:
        # compute angle to fruit
        snake_x, snake_y = snake.pos[0]
        angle = math.atan2(apple.pos[0] - snake_x, apple.pos[1] - snake_y)

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

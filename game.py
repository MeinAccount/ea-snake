import random
import time
from typing import Callable

import pygame
from pygame.constants import K_ESCAPE

# directions:
# - right 0
# - top 1
# - left 2
# - down 3


GRID_WIDTH = 50
GRID_HEIGHT = 50


class Apple:
    pos = (0, 0)
    direction = 0

    def __init__(self) -> None:
        self.replace()

    def replace(self):
        self.pos = (random.randint(0, GRID_WIDTH), random.randint(0, GRID_HEIGHT))

    def draw(self, surface, image):
        surface.blit(image, (self.pos[0] * 10, self.pos[1] * 10))


def direction_apply(direction, pos):
    (x, y) = pos
    if direction == 0:
        return x + 1, y
    if direction == 1:
        return x, y - 1
    if direction == 2:
        return x - 1, y
    if direction == 3:
        return x, y + 1


class Snake:
    pos = []
    current_direction = 0

    def __init__(self, start_pos, length=3) -> None:
        self.length = length
        self.pos.append(start_pos)
        for i in range(1, length):
            self.pos.append(direction_apply(2, self.pos[i - 1]))

    def draw(self, surface, image):
        for (x, y) in self.pos:
            surface.blit(image, (x * 10, y * 10))

    def move(self, apple: Apple) -> bool:
        new_pos = direction_apply(self.current_direction, self.pos[0])
        if apple.pos == new_pos:
            apple.replace()
        else:
            self.pos.pop()

        if new_pos in self.pos:
            return False  # self intersection!

        self.pos.insert(0, new_pos)
        return True


class App:
    windowWidth = GRID_WIDTH * 10
    windowHeight = GRID_HEIGHT * 10

    # step handler takes the snake and the apple and returns a new direction
    def __init__(self, step_handler: Callable[[Snake, Apple], int]) -> None:
        self.step_handler = step_handler

        self.apple = Apple()
        self.snake = Snake((20, 20))

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)

        pygame.display.set_caption('EA Snake')
        # self._image_surf = pygame.image.load("pygame.png").convert()
        # self._apple_surf = pygame.image.load("apple.png").convert()
        self._image_surf = pygame.Surface((10, 10))
        self._image_surf.fill((255, 0, 0))

        self._apple_surf = pygame.Surface((10, 10))
        self._apple_surf.fill((0, 255, 0))

    def on_loop(self) -> bool:
        self.snake.current_direction = self.step_handler(self.snake, self.apple)

        # move
        if not self.snake.move(self.apple):
            print("self intersection!!!")
            return False

        # TODO: check for edges

        return True

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        self.snake.draw(self._display_surf, self._image_surf)
        self.apple.draw(self._display_surf, self._apple_surf)
        pygame.display.flip()

    def on_execute(self):
        self.on_init()
        running = True
        while running:
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if keys[K_ESCAPE]:
                running = False

            running = self.on_loop()
            self.on_render()
            time.sleep(50.0 / 1000.0)
        pygame.quit()


class SimpleHandler:
    directions = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]
    index = 0

    def handle(self, snake, apple):
        self.index = (self.index + 1) % len(self.directions)
        return self.directions[self.index]


if __name__ == "__main__":
    theApp = App(SimpleHandler().handle)
    theApp.on_execute()

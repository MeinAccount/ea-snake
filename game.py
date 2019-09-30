import time
from typing import Callable

import pygame
from pygame.constants import K_ESCAPE

from data import Snake, Apple, GRID_HEIGHT, GRID_WIDTH


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
            else:
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

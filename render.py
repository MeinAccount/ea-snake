from typing import Callable

import pygame
from pygame.constants import K_ESCAPE, K_SPACE, KEYDOWN, QUIT

from game.data import Snake, Apple, GRID_HEIGHT, GRID_WIDTH


class App:
    windowWidth = GRID_WIDTH * 10
    windowHeight = GRID_HEIGHT * 10

    # step handler takes the snake and the apple and returns a new direction
    def __init__(self, step_handler: Callable[[Snake, Apple], int]) -> None:
        self.step_handler = step_handler

        self.snake = Snake((20, 20))
        self.apple = Apple()
        self.apple.pos = (22, 20)

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
            print("self or border intersection")
            return False

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
            self.on_render()
            event = pygame.event.wait()
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False
            elif event.type == KEYDOWN and event.key == K_SPACE:
                running = self.on_loop()

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

from typing import Callable

import pygame
from pygame.constants import K_ESCAPE, K_SPACE, KEYDOWN, QUIT, USEREVENT, K_p, K_r

from game.direction import GRID_WIDTH, GRID_HEIGHT
from game.state import GameState


class App:
    windowWidth = GRID_WIDTH * 10
    windowHeight = GRID_HEIGHT * 10

    # step handler takes the snake and the apple and returns a new direction
    def __init__(self, step_handler: Callable[[GameState], int],
                 tick_handler: Callable[[], None] = lambda: None) -> None:
        self.step_handler = step_handler
        self.tick_handler = tick_handler

        self.state = GameState((20, 20))
        self.state.apple_pos = (22, 20)

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
        self.state.direction = self.step_handler(self.state)

        # move
        if not self.state.move():
            print("self or border intersection")
            return False

        return True

    def on_render(self):
        self._display_surf.fill((0, 0, 0))

        # draw apple
        self._display_surf.blit(self._apple_surf, (self.state.apple_pos[0] * 10, self.state.apple_pos[1] * 10))

        # draw tiles
        for (x, y) in self.state.positions:
            self._display_surf.blit(self._image_surf, (x * 10, y * 10))
        pygame.display.flip()

    EVENT_TICK = USEREVENT + 1

    def on_execute(self):
        self.on_init()
        pygame.time.set_timer(self.EVENT_TICK, 100)

        running = True
        playing = False
        while running:
            self.on_render()
            event = pygame.event.wait()
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False
            elif event.type == KEYDOWN and event.key == K_SPACE:
                self.on_loop()
            elif event.type == self.EVENT_TICK:
                self.tick_handler()
                if playing:
                    playing = self.on_loop()
            elif event.type == KEYDOWN and event.key == K_p:
                playing = not playing
            elif event.type == KEYDOWN and event.key == K_r:
                self.state = GameState((20, 20))
                self.state.apple_pos = (22, 20)

        pygame.quit()


class SimpleHandler:
    directions = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]
    index = 0

    def handle(self, state):
        self.index = (self.index + 1) % len(self.directions)
        return self.directions[self.index]


if __name__ == "__main__":
    theApp = App(SimpleHandler().handle)
    theApp.on_execute()

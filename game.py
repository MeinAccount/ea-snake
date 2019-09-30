import time

import pygame
# directions:
# - right 0
# - top 1
# - left 2
# - down 3
from pygame.constants import K_ESCAPE


class Apple:
    x = 0
    y = 0
    direction = 0

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))


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

    def move(self):
        self.pos.insert(0, direction_apply(self.current_direction, self.pos[0]))
        self.pos.pop()
        print(self.pos)


class App:
    grindWidth = 50
    gridHeight = 50

    def __init__(self) -> None:
        self.windowWidth = self.grindWidth * 10
        self.windowHeight = self.gridHeight * 10

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

            self.snake.move()
            self.on_render()

            time.sleep(50.0 / 1000.0)
        # pygame.quit()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()

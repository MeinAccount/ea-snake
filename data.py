import random

GRID_WIDTH = 50
GRID_HEIGHT = 50


# directions:
# - right 0
# - top 1
# - left 2
# - down 3

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

        # check for edge
        if new_pos[0] == -1 or new_pos[0] == GRID_WIDTH or new_pos[1] == -1 or new_pos == GRID_HEIGHT:
            return False

        # check for apple
        if apple.pos == new_pos:
            self.length += 1
            apple.replace()
        else:
            self.pos.pop()

        # check for self intersection
        if new_pos in self.pos:
            return False

        # insert new pos
        self.pos.insert(0, new_pos)
        return True

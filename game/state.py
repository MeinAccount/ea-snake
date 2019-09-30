import random

from game.direction import Directions, GRID_WIDTH, GRID_HEIGHT


class GameState:
    apple_pos = (0, 0)
    positions = None
    direction = 0

    def __init__(self, start_pos, length=3) -> None:
        self.length = length
        self.positions = [start_pos]
        for i in range(1, length):
            self.positions.append(Directions.apply(2, self.positions[i - 1]))

        self.apple_replace()

    def move(self) -> bool:
        new_pos = Directions.apply(self.direction, self.positions[0])

        # check for edge
        if new_pos[0] == -1 or new_pos[0] == GRID_WIDTH or new_pos[1] == -1 or new_pos[1] == GRID_HEIGHT:
            return False

        # check for apple
        if self.apple_pos == new_pos:
            self.length += 1
            self.apple_replace()
        else:
            self.positions.pop()

        # check for self intersection
        self_intersection = new_pos in self.positions
        self.positions.insert(0, new_pos)
        return not self_intersection

    def apple_replace(self):
        self.apple_pos = (random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT))

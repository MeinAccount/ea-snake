# directions:
# - right 0
# - top 1
# - left 2
# - down 3


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

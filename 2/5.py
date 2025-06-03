import math


def count_shortest_paths(width, height):
    return math.comb(width + height, width)


def count_paths_no_consecutive_up(width, height):
    if height > width + 1:
        return 0
    return math.comb(width + 1, height)


print(count_shortest_paths(20, 18))
print(count_paths_no_consecutive_up(20, 18))

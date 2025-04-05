import math


def count_shortest_paths(horizontal_steps, vertical_steps):
    n = horizontal_steps + vertical_steps
    k = horizontal_steps
    return math.comb(n, k)


# количество различных кратчайших путей
horizontal_steps = 20
vertical_steps = 18
total_paths = count_shortest_paths(horizontal_steps, vertical_steps)
print(f"Общее количество кратчайших путей: {total_paths}")


# количество различных кратчайших путей с ограничением на вертикальные участки
def count_restricted_paths(horizontal_steps, vertical_steps):

    paths = [[0] * (vertical_steps + 1) for _ in range(horizontal_steps + 1)]
    paths[0][0] = 1

    for h in range(horizontal_steps + 1):
        for v in range(vertical_steps + 1):
            if h > 0:
                paths[h][v] += paths[h - 1][v]
            if v > 0:
                paths[h][v] += paths[h][v - 1]
            if h > 0 and v > 0:
                paths[h][v] -= paths[h - 1][v - 1]

    return paths[horizontal_steps][vertical_steps]


restricted_paths = count_restricted_paths(horizontal_steps, vertical_steps)
print(f"Количество кратчайших путей с ограничением: {restricted_paths}")

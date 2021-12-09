#!/usr/bin/env python3

import math
from typing import Set, Tuple


def is_low_point(row, col, data):
    return all([data.get(c, float('inf')) > data[(row, col)]
                for c in neighbors(row, col)])


def neighbors(row, col):
    return [(row-1, col), (row+1, col), (row, col+1), (row, col-1)]


def compute_basin(row, col, data) -> Set[Tuple[int, int]]:
    points = set()
    to_process = set([(row, col)])
    while to_process:
        e = to_process.pop()
        if e in points:
            continue

        for n in neighbors(*e):
            if n in points:
                continue

            elif data.get(n, float('inf')) < 9:
                to_process.add(n)
        points.add(e)

    return points


if __name__ == '__main__':
    data = {}
    with open('input', 'r') as h:
        for row, line in enumerate(h):
            for col, x in enumerate(line.strip()):
                data[(row, col)] = int(x)

    low_points = [data[x] for x in data.keys() if is_low_point(*x, data)]
    print('Part 1 -> ', sum(low_points) + len(low_points))

    low_points = [x for x in data.keys() if is_low_point(*x, data)]
    basins = sorted([len(compute_basin(*p, data)) for p in low_points], reverse=True)
    print('Part 2 -> ', math.prod(basins[:3]))

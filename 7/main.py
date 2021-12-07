#!/usr/bin/env python3

import functools


@functools.cache
def steps_to_fuel(step):
    return sum([c+1 for (c, _) in enumerate(range(step))])


if __name__ == '__main__':
    with open('input', 'r') as h:
        positions = list(map(int, h.readline().strip().split(',')))

    res = {}
    mi = min(positions)
    ma = max(positions)
    for i in range(mi, ma+1):
        res[i] = sum([abs(p-i) for p in positions])

    w = min(res.items(), key=lambda x: x[1])
    print('Part 1 -> ', w[1])

    res = {}
    for i in range(mi, ma+1):
        res[i] = sum([steps_to_fuel(abs(p-i)) for p in positions])

    w = min(res.items(), key=lambda x: x[1])
    print('Part 2 -> ', w[1])

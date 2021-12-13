#!/usr/bin/env python3

import re
from typing import Tuple, Set


dot_line = re.compile(r'(\d+),(\d+)')
fold_line = re.compile(r'^fold along (\w+)=(\d+)')
x = 0
y = 1


def fold(axis: str, fold: int, space: Set[Tuple[int, int]]):
    dim = x if axis == 'x' else y
    points = list(filter(lambda x: x[dim] > fold, space))

    for p in points:
        new_v = fold + (fold - p[dim])
        new_p = (p[0], new_v) if dim == y else (new_v, p[1])
        space.add(new_p)
        space.remove(p)


def display_space(space: Set[Tuple[int, int]]):
    mr = max(space, key=lambda e: e[y])[y]+1
    mc = max(space, key=lambda e: e[x])[x]+1

    matrix = [[' ' for _ in range(mc)] for _ in range(mr)]
    for (c, r) in space:
        matrix[r][c] = '#'

    return '\n'.join(map(lambda e: ''.join(e), matrix))


if __name__ == '__main__':
    dots = set()
    folds = []

    with open('input', 'r') as h:
        for ln in h.readlines():
            if m := dot_line.match(ln):
                r, c = map(int, m.groups())
                dots.add((r, c))
            elif m := fold_line.match(ln):
                ax, v = m.groups()
                folds.append((ax, int(v)))

    fold(*folds[0], dots)
    print(f'Part 1 -> {len(dots)}')

    for f in folds[1:]:
        fold(*f, dots)

    print('Part 2 ->')
    print(display_space(dots))

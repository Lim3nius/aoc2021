

import re
from collections import defaultdict
from typing import Dict, Tuple


dot_line = re.compile(r'(\d+),(\d+)')
fold_line = re.compile(r'^fold along (\w+)=(\d+)')
x = 0
y = 1


def fold(axis: str, fold: int, space: Dict[Tuple[int, int], bool]) -> Dict[Tuple[int, int], bool]:
    dim = x if axis == 'x' else y
    points = list(filter(lambda x: x[dim] > fold, space.keys()))
    to_copy = list(filter(lambda x: x[dim] < fold, space.keys()))

    new_space = {}
    for p in points:
        new_v = fold + (fold - p[dim])

        new_p = (p[0], new_v) if dim == y else (new_v, p[1])
        new_space[new_p] = True

    for p in to_copy:
        new_space[p] = True

    return new_space


def display_space(space: Dict[Tuple[int, int], bool]):
    mr = max(space.keys(), key=lambda e: e[y])[y]+1
    mc = max(space.keys(), key=lambda e: e[x])[x]+1

    matrix = [['.' for _ in range(mc)] for _ in range(mr)]
    for (c, r) in space.keys():
        matrix[r][c] = '#'

    return '\n'.join(map(lambda e: ' '.join(e), matrix))


if __name__ == '__main__':
    dots = dict()
    folds = []

    with open('input', 'r') as h:
        for ln in h.readlines():
            if m := dot_line.match(ln):
                r, c = map(int, m.groups())
                dots[(r, c)] = True
            elif m := fold_line.match(ln):
                ax, v = m.groups()
                folds.append((ax, int(v)))

    dots = fold(*folds[0], dots)
    print(f'Part 1 -> {len(dots)}')

    for f in folds[1:]:
        dots = fold(*f, dots)

    print(display_space(dots))

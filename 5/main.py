#!/usr/bin/env python3

from collections import defaultdict
from typing import List, Tuple


def connect_pts(ln: List[Tuple[int, int]]):
    p0, p1 = ln
    x, y = 0, 1
    pts = []
    sx = sign(p1[x] - p0[x])
    sy = sign(p1[y] - p0[y])
    tmp = [p0[x], p0[y]]
    pts.append(p0)
    while not((tmp[x] == p1[x]) and (tmp[y] == p1[y])):
        tmp[x] += sx
        tmp[y] += sy
        pts.append((tmp[x], tmp[y]))
    return pts


def sign(x):
    if x == 0:
        return 0
    elif x < 0:
        return -1
    else:
        return 1


def line_points(ln: List[Tuple[int, int]]):
    p0, p1 = ln
    x, y = 0, 1
    if p0[x] == p1[x] or p0[y] == p1[y]:
        return connect_pts(ln)
    else:
        return []


def diagonal_points(ln: List[Tuple[int, int]]):
    p0, p1 = ln
    x, y = 0, 1

    if p0[x] == p1[x] or p0[y] == p1[y]:
        return []
    else:
        return connect_pts(ln)


if __name__ == '__main__':
    data = []
    with open('input', 'r') as h:
        for ln in h:
            p0, p1 = ln.split('->')
            p0 = tuple(map(int, p0.split(',')))
            p1 = tuple(map(int, p1.split(',')))
            data.append([p0, p1])

    covered_points = defaultdict(int)
    for ln in data:
        for pts in line_points(ln):
            covered_points[pts] += 1

    overlap = list(filter(lambda v: v[1] > 1, covered_points.items()))
    print('Part 1 -> ', len(overlap))

    for ln in data:
        for pts in diagonal_points(ln):
            covered_points[pts] += 1

    overlap = list(filter(lambda v: v[1] > 1, covered_points.items()))
    print('Part 2 -> ', len(overlap))

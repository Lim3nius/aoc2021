#!/usr/bin/env python3

from typing import List, Tuple, Iterable


x = 1
y = 0
dim = 0


def neighbors(p: Tuple[int, int]) -> Iterable[Tuple[int, int]]:
    return filter(lambda e: all(0 <= e[i] < dim for i in [x, y]),
                  [(p[0]+x, p[1] + y) for (x, y) in [(-1, 0), (1, 0), (0, 1), (0, -1)]])


def find_shortest(matrix, matrix2):
    start = (0, 0)
    to_process = set([start])

    while to_process:
        p = to_process.pop()
        for n in neighbors(p):
            prev = matrix2[n[x]][n[y]]
            matrix2[n[x]][n[y]] = min(matrix2[p[x]][p[y]] + matrix[n[x]][n[y]],
                                      matrix2[n[x]][n[y]])

            if prev != matrix2[n[x]][n[y]]:
                to_process.add(n)
    return


def inc_matrix(m: List[List[int]], add=1) -> List[List[int]]:
    return [[v + add if v + add < 10 else v + add - 9 for v in row] for row in m]


def append_to_matrix_horizontally(m0, m1: List[List[int]]) -> List[List[int]]:
    m = [[] for _ in range(len(m0))]
    for r in range(len(m0)):
        m[r] = [*m0[r], *m1[r]]

    return m


def spread_matrix(m: List[List[int]]) -> List[List[int]]:
    new_m = [[], [], [], [], []]
    for r in range(5):
        new_mr = inc_matrix(m, r)
        for c in range(4):
            new_mr = append_to_matrix_horizontally(new_mr, inc_matrix(m, r+c+1))
        new_m[r] = new_mr

    new = new_m[0]
    for i in range(dim, dim*5):
        new.append(new_m[i // dim][i % dim])

    return new


def control_matrix(fpath: str, matrix: List[List[int]]):
    with open(fpath, 'r') as h:
        control = [[int(c) for c in line.strip()] for line in h]

    for r in range(len(matrix)):
        for c in range(len(matrix[r])):
            if matrix[r][c] != control[r][c]:
                print(f'Diff at: ({r}, {c}) -> {matrix[r][c]} != {control[r][c]}')


def format_matrix(m: List[List[int]]) -> str:
    return '\n'.join([''.join(map(str, r)) for r in m])


if __name__ == '__main__':
    with open('input', 'r') as h:
        matrix = [[int(c) for c in line.strip()] for line in h]
    dim = len(matrix[0])

    matrix2 = [[float('inf') for _ in range(len(ln))] for ln in matrix]
    matrix2[0][0] = 0
    find_shortest(matrix, matrix2)
    print(f'Part 1 -> {matrix2[-1][-1]}')

    matrix = spread_matrix(matrix)
    dim = len(matrix[0])

    matrix2 = [[float('inf') for _ in range(len(ln))] for ln in matrix]
    matrix2[0][0] = 0
    find_shortest(matrix, matrix2)
    print(f'Part 2 -> {matrix2[-1][-1]}')

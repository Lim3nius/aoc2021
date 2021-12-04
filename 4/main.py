#!/usr/bin/env python3

from typing import List, Tuple


class Matrix:
    def __init__(self, data_m):
        self.data_m = data_m
        self.marked_m = [[0 for _ in ll] for ll in data_m]

    def reset(self):
        self.marked_m = [[0 for _ in ll] for ll in self.marked_m]

    def __str__(self):
        ln = ''
        for i in range(len(self.data_m)):
            ln += ' '.join([f'{c: 3}' for c in self.data_m[i]])
            ln += '\t'
            ln += ' '.join([f'{c: 3}' for c in self.marked_m[i]])
            ln += '\n'

        return ln

    def won(self):
        for ln in self.marked_m:
            if all(ln):
                return True

        for i in range(len(self.marked_m)):
            if all([ln[i] for ln in self.marked_m]):
                return True

        return False

    def accept(self, d):
        for r in range(len(self.marked_m)):
            for c in range(len(self.marked_m[r])):
                if self.data_m[r][c] == d:
                    self.marked_m[r][c] = 1

    def unmarked(self):
        res = []
        for r in range(len(self.marked_m)):
            for c in range(len(self.marked_m[r])):
                if self.marked_m[r][c] == 0:
                    res.append(self.data_m[r][c])
        return res


if __name__ == '__main__':
    with open('input', 'r') as h:
        nums = [int(n) for n in h.readline().strip().split(',')]
        matrixes = []
        m = []
        h.readline()  # remove empty line
        for line in h:
            if line.strip() == '':
                matrixes.append(Matrix(m))
                m = []
            else:
                m.append([int(c) for c in filter(
                    lambda f: f != '', line.strip().split(' '))])
        matrixes.append(Matrix(m))

    def play(numbers: List[int], matrixes: List[Matrix]) -> List[Tuple[int, int]]:
        '''play numbers till all matrixes are won, return tuples containing unmarked sum & winning number'''
        winners = []
        finished = set()
        for c in numbers:
            for i in range(len(matrixes)):
                if i in finished:
                    continue

                matrixes[i].accept(c)
                if matrixes[i].won():
                    winners.append((sum(matrixes[i].unmarked()), c))
                    finished.add(i)

            if len(winners) == len(matrixes):
                return winners

    winners = play(nums, matrixes)
    print(f'Part 1: {winners[0][0] * winners[0][1]}')
    print(f'Part 2: {winners[-1][0] * winners[-1][1]}')

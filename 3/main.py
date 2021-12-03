#!/usr/bin/env python3

import collections
from typing import List, Callable


def find_common(numbers: List[List[int]], comparison: str):
    def inner(numbers, pos) -> List[List[int]]:
        if len(numbers) == 1:
            return numbers[0]

        cmp = collections.defaultdict(int)
        for n in numbers:
            cmp[n[pos]] += 1

        if cmp[0] > cmp[1]:
            want_val = 0
        else:
            want_val = 1

        if comparison == 'min':
            want_val = 1 if want_val == 0 else 0

        if cmp[0] == cmp[1]:
            want_val = 1 if comparison == 'max' else 0

        next_nums = []
        for n in numbers:
            if n[pos] == want_val:
                next_nums.append(n)

        return inner(next_nums, pos+1)
    return inner(numbers, 0)


if __name__ == '__main__':
    numbers = []
    with open('input', 'r') as h:
        for ln in h:
            numbers.append([int(x) for x in ln.strip()])

    bits = len(numbers[0])
    position_stats = [collections.defaultdict(int) for _ in range(bits)]
    for n in numbers:
        for i in range(bits):
            position_stats[i][n[i]] += 1

    mst_cmn = []
    lst_cmn = []
    for pos in position_stats:
        if pos[0] > pos[1]:
            mst_cmn.append(1)
            lst_cmn.append(0)
        else:
            mst_cmn.append(0)
            lst_cmn.append(1)

    mst_num = int(''.join(map(str, mst_cmn)), 2)
    lst_num = int(''.join(map(str, lst_cmn)), 2)

    print(f'Part1: {mst_num * lst_num}')

    oxygen = find_common(numbers[:], 'max')
    co2 = find_common(numbers[:], 'min')

    oxygen = int(''.join(map(str, oxygen)), 2)
    co2 = int(''.join(map(str, co2)), 2)

    print(f'Part2: {oxygen * co2}')

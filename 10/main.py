#!/usr/bin/env python3


from typing import Tuple
from functools import reduce


pairs = {
    '(': ')',
    '{': '}',
    '[': ']',
    '<': '>',
}

opening = set(pairs.keys())
closing = set(pairs.values())

err_to_points = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

missing_to_points = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


def check_line(ln) -> Tuple[bool, Tuple[str, str]]:
    ''''checks if line is syntactically correct. Return bool if is,
    and tuple(expected, got)
    '''
    stack = []
    for c in ln:
        if c in opening:
            stack.append(c)
        elif c in closing:
            if pairs[stack[-1]] == c:
                stack.pop()
            else:
                return False, (stack[-1], c, stack)

    if len(stack) == 0:
        return True, (),
    else:
        return False, (stack[-1], None, stack)


if __name__ == '__main__':
    with open('input', 'r') as h:
        data = [ln.strip() for ln in h.readlines()]

    incomplete = []
    acc = 0
    for ln in data:
        ok, res = check_line(ln)
        if not ok and res[1] is not None:
            acc += err_to_points[res[1]]
        if not ok and res[1] is None:
            incomplete.append(res[2])

    print('Part 1 -> ', acc)

    scores = []
    for ln in incomplete:
        points = [missing_to_points[pairs[c]] for c in ln[::-1]]
        points.insert(0, 0)
        scores.append(reduce(lambda acc, e: acc*5 + e, points))

    scores = sorted(scores)
    print('Part 2 -> ', scores[len(scores) // 2])

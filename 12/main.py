#!/usr/bin/env python3

from collections import defaultdict
from string import ascii_lowercase
from typing import Dict, List


def is_small(c):
    return all(map(lambda x: x in ascii_lowercase, c))


def traverse(cave_segments: Dict[str, List[str]], small_cave_repetition: bool) -> List[List[str]]:
    paths = []

    def inner(pos: str,
              visited: List[str],
              paths: List[List[str]],
              small_cave_double_visited: bool) -> None:
        if pos == 'end':
            paths.append(list(visited))
            return

        for p in cave_segments[pos]:
            if is_small(p):
                if not small_cave_repetition and p in visited:
                    continue

                if small_cave_repetition and p in visited:
                    if small_cave_double_visited or p in ['start', 'end']:
                        continue
                    else:
                        inner(p, [*visited, p], paths, True)
                        continue

            inner(p, [*visited, p], paths, small_cave_double_visited)

    inner('start', ['start'], paths, False)
    return paths


if __name__ == '__main__':
    segments = defaultdict(list)
    with open('input', 'r') as h:
        for ln in h:
            s, e = ln.strip().split('-')
            segments[s].append(e)
            segments[e].append(s)

    paths = traverse(segments, False)
    print(f'Part 1 -> {len(paths)}')

    paths = traverse(segments, True)
    print(f'Part 2 -> {len(paths)}')

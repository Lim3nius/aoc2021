#!/usr/bin/env python3

states = {}
iter_cnt = 18


def simulate_fish(init_s: int, iters: int) -> int:
    alt_iters = max(0, iters - init_s)

    if r := states.get((alt_iters, 0), None):
        return r

    childs = []
    for c in range(0, alt_iters, 7):
        childs.append((8, alt_iters - c - 1))

    sub_childs = sum([simulate_fish(*c) for c in childs])
    childs_total = sub_childs + len(childs)
    states[(alt_iters, 0)] = childs_total
    return childs_total


if __name__ == '__main__':
    with open('input', 'r') as h:
        fish_init = list(map(int, h.readline().split(',')))

    res_fish = sum([simulate_fish(f, 80)+1 for f in fish_init])
    print(f'Part 1 -> {res_fish}')

    states = {}
    res = sum([simulate_fish(f, 256)+1 for f in fish_init])
    print(f'Part 2 -> {res}')

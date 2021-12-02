#!/usr/bin/env python3

if __name__ == '__main__':
    instructions = []
    state = {
        'depth': 0,
        'pos': 0
    }

    with open('input', 'r') as h:
        for ln in h:
            d, v = ln.strip().split(' ')
            v = int(v)
            instructions.append((d, v))

    for (d, v) in instructions:
        if d == 'up':
            state['depth'] -= v
        elif d == 'down':
            state['depth'] += v
        elif d == 'forward':
            state['pos'] += v

    print(f'Part 1: {state["depth"] * state["pos"]}')

    state = {
        'depth': 0,
        'pos': 0,
        'aim': 0
    }

    for (d, v) in instructions:
        if d == 'up':
            state['aim'] -= v
        elif d == 'down':
            state['aim'] += v
        elif d == 'forward':
            state['pos'] += v
            state['depth'] += state['aim'] * v

    print(f'Part 2: {state["depth"] * state["pos"]}')

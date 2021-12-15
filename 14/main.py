#!/usr/bin/env python3

from typing import Dict, Tuple


def states_to_elements(states: Dict[str, int], first_pair: str) -> Dict[str, int]:
    elements = {}
    for k, c in states.items():
        if k == first_pair:
            elements[k[0]] = elements.get(k[0], 0) + 1
        elements[k[1]] = elements.get(k[1], 0) + c

    return elements


def polymer_insertion(rules: Dict[str, str], state: Dict[str, int], first_pair: str) -> Tuple[Dict[str, int], str]:
    new_state = {k: 0 for k in rules}
    new_fpair = ''
    for (k, c) in state.items():
        new = rules[k]
        new_state[f'{k[0]}{new}'] += c
        new_state[f'{new}{k[1]}'] += c
        if k == first_pair:
            new_fpair = f'{k[0]}{new}'

    return new_state, new_fpair


def do_x_steps(steps: int, rules: Dict[str, str], state: Dict[str, int], first_pair: str) -> int:
    for _ in range(steps):
        state, first_pair = polymer_insertion(rules, state, first_pair)

    elems = states_to_elements(state, first_pair)
    mx = max(elems.items(), key=lambda k: k[1])[1]
    mn = min(elems.items(), key=lambda k: k[1])[1]
    return mx - mn


if __name__ == '__main__':
    rules = {}

    with open('input', 'r') as h:
        init = h.readline().strip()
        h.readline()

        for ln in h.readlines():
            _in, out = ln.strip().split(' -> ')
            rules[_in] = out

    states = {k: 0 for k in rules}
    for k in range(0, len(init)-1):
        states[init[k:k+2]] += 1

    first_pair = init[:2]

    print('Part 1 -> ', do_x_steps(10, rules, states, first_pair))
    print('Part 2 -> ', do_x_steps(40, rules, states, first_pair))

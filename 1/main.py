#!/usr/bin/env python3

if __name__ == '__main__':
    data = []
    with open('input', 'r') as h:
        for ln in h:
            data.append(int(ln.strip()))

    inc = 0
    for i in range(1, len(data)):
        if data[i] > data[i-1]:
            inc += 1

    print(f'Part 1: {inc}')

    inc = 0
    for i in range(1, len(data)-2):
        if sum(data[i:i+3]) > sum(data[i-1:i+2]):
            inc += 1

    print(f'Part 2: {inc}')

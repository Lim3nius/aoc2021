

DIM = 10


def in_grid(loc):
    return all([0 <= loc[p] < DIM for p in [0, 1]])


def neighbors_location(x, y):
    return filter(lambda x: in_grid(x), [(x+r, y+c)
                                         for r in [-1, 0, 1]
                                         for c in [-1, 0, 1]])


def to_matrix(locations):
    d = []
    for r in range(DIM):
        d.append(' '.join(map(str, [locations[(r, c)] for c in range(DIM)])))
    return '\n'.join(d)


def step(matrix):
    flashed = set()
    to_flash = set()

    for (loc, v) in matrix.items():
        if v >= 9:
            to_flash.add(loc)
        matrix[loc] = (v + 1) % 10

    while to_flash:
        loc = to_flash.pop()
        for nloc in neighbors_location(*loc):
            v = matrix[nloc]
            if nloc in flashed:
                continue
            matrix[nloc] = (v + 1) % 10
            if matrix[nloc] == 0:
                to_flash.add(nloc)

        matrix[loc] = 0
        flashed.add(loc)

    return len(flashed)


if __name__ == '__main__':
    data = {}
    with open('input', 'r') as h:
        for r, ln in enumerate(h.readlines()):
            DIM = len(ln.strip())
            for c, v in enumerate(ln.strip()):
                data[(r, c)] = int(v)

    print(to_matrix(data)+'\n')

    steps = 100
    flashes = sum([step(data) for _ in range(steps)])
    print(f'Part 1 -> {flashes}')

    i = 0
    while True:
        i += 1
        flashes = step(data)
        if flashes == len(data):
            break

    print(f'Part 2 -> {i+steps}')

from collections import defaultdict
from itertools import product
from typing import Set, Tuple


def input_parser(path: str, dims: int) -> Set[Tuple[int, ...]]:
    pad_zeros = (0,) * (dims - 2)
    actives = set()
    with open(path) as f:
        for y, line in enumerate(f.readlines()):
            for x, char in enumerate(line):
                if char == '#':
                    actives.add((x, y) + pad_zeros)
    return actives


def one_iter(actives: Set[Tuple[int, ...]], add) -> Set[Tuple[int, ...]]:
    dims = len(next(iter(actives)))
    zeros = (0,) * dims
    cnt_active_neighbors = defaultdict(int)
    for coords in actives:
        for d_coords in product((-1, 0, 1), repeat=dims):
            if d_coords == zeros:
                continue
            cnt_active_neighbors[add(coords, d_coords)] += 1
            # Significantly slower: cnt_active_neighbors[tuple([x + dx for x, dx in zip(coords, d_coords)])] += 1

    new_actives = set()
    for coords, cnt in cnt_active_neighbors.items():
        if coords in actives and cnt in (2, 3):
            new_actives.add(coords)
        elif coords not in actives and cnt == 3:
            new_actives.add(coords)

    return new_actives


def solve(actives: Set[Tuple[int, ...]], add) -> int:
    for _ in range(6):
        actives = one_iter(actives, add)
    return len(actives)


def add_3(coords, d_coords):
    return coords[0] + d_coords[0], coords[1] + d_coords[1], coords[2] + d_coords[2]


def add_4(coords, d_coords):
    return coords[0] + d_coords[0], coords[1] + d_coords[1], coords[2] + d_coords[2], coords[3] + d_coords[3]


print(solve(input_parser("inputs/17.txt", 3), add_3))
print(solve(input_parser("inputs/17.txt", 4), add_4))

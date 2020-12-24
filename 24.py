from collections import defaultdict
from re import compile as reg_compile
from typing import List, Set, Tuple


def input_reader(path: str) -> List[List[str]]:
    with open(path) as f:
        lines = f.read(-1).split()
    reg = reg_compile('e|se|sw|w|nw|ne')
    return [reg.findall(line) for line in lines]


def traverse_to_tile(steps: List[str]) -> Tuple[int, int]:
    # https://www.redblobgames.com/grids/hexagons/#coordinates-axial
    q = r = 0
    for step in steps:
        if step == 'e':
            q -= 1
        elif step == 'se':
            q -= 1
            r += 1
        elif step == 'sw':
            r += 1
        elif step == 'w':
            q += 1
        elif step == 'nw':
            q += 1
            r -= 1
        elif step == 'ne':
            r -= 1
    return q, r


def initial_black_tiles(tiles_steps: List[List[str]]) -> Set[Tuple[int, int]]:
    black_tiles = set()
    for steps in tiles_steps:
        pos = traverse_to_tile(steps)
        if pos in black_tiles:
            black_tiles.remove(pos)
        else:
            black_tiles.add(pos)
    return black_tiles


def one_iter(black_pos: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    cnt_black_adjacent = defaultdict(int)
    for q, r in black_pos:
        cnt_black_adjacent[q + 1, r] += 1
        cnt_black_adjacent[q - 1, r] += 1
        cnt_black_adjacent[q, r + 1] += 1
        cnt_black_adjacent[q, r - 1] += 1
        cnt_black_adjacent[q + 1, r - 1] += 1
        cnt_black_adjacent[q - 1, r + 1] += 1

    new_blacks = set()

    for tile in black_pos:
        if cnt_black_adjacent.get(tile, 0) in (1, 2):
            new_blacks.add(tile)

    for tile, cnt in cnt_black_adjacent.items():
        if tile not in black_pos and cnt == 2:
            new_blacks.add(tile)

    return new_blacks


def solve_a(tiles_steps: List[List[str]]) -> Tuple[Set[Tuple[int, int]], int]:
    black_tiles = initial_black_tiles(tiles_steps)
    return black_tiles, len(black_tiles)


def solve_b(black_pos: Set[Tuple[int, int]]) -> int:
    for _ in range(100):
        black_pos = one_iter(black_pos)
    return len(black_pos)


data = input_reader("inputs/24.txt")
positions, count = solve_a(data)
print(count)
print(solve_b(positions))

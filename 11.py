import copy
from itertools import chain
from typing import Callable, List

FLOOR = 0
EMPTY = 1
OCCUPIED = 2


def input_reader(path: str) -> str:
    with open(path) as f:
        return f.read(-1)


def parse_input(data: str) -> List[List[int]]:
    rows = data.replace('L', str(EMPTY)).replace('.', str(FLOOR)).split()
    return [[int(i) for i in row] for row in rows]


def one_iter(curr: List[List[int]], out: List[List[int]], limit: int, counter: Callable) -> bool:
    changes = False
    max_row, max_col = len(curr), len(curr[0])

    for row in range(max_row):
        for col in range(max_col):
            curr_seat = curr[row][col]
            if curr_seat == FLOOR:
                continue

            occupied_around = counter(curr, row, col, max_row, max_col)
            if curr_seat == EMPTY and occupied_around == 0:
                changes = True
                out[row][col] = OCCUPIED
            elif curr_seat == OCCUPIED and occupied_around >= limit:
                changes = True
                out[row][col] = EMPTY
            else:
                out[row][col] = curr_seat
    return changes


def count_near(curr: List[List[int]], row: int, col: int, max_row: int, max_col: int) -> int:
    occupied_around = 0

    if row > 0:
        occupied_around += curr[row - 1][col] == OCCUPIED
        if col > 0:
            occupied_around += curr[row - 1][col - 1] == OCCUPIED
        if col < max_col - 1:
            occupied_around += curr[row - 1][col + 1] == OCCUPIED

    if col > 0:
        occupied_around += curr[row][col - 1] == OCCUPIED
    if col < max_col - 1:
        occupied_around += curr[row][col + 1] == OCCUPIED

    if row < max_row - 1:
        occupied_around += curr[row + 1][col] == OCCUPIED
        if col > 0:
            occupied_around += curr[row + 1][col - 1] == OCCUPIED
        if col < max_col - 1:
            occupied_around += curr[row + 1][col + 1] == OCCUPIED
    return occupied_around


def count_far(curr: List[List[int]], row: int, col: int, max_row: int, max_col: int) -> int:
    return (search_dir(curr, row, col, 1, -1, max_row, max_col)
            + search_dir(curr, row, col, 1, 0, max_row, max_col)
            + search_dir(curr, row, col, 1, 1, max_row, max_col)
            + search_dir(curr, row, col, 0, -1, max_row, max_col)
            + search_dir(curr, row, col, 0, 1, max_row, max_col)
            + search_dir(curr, row, col, -1, -1, max_row, max_col)
            + search_dir(curr, row, col, -1, 1, max_row, max_col)
            + search_dir(curr, row, col, -1, 0, max_row, max_col))


def search_dir(curr: List[List[int]], row: int, col: int, dx: int, dy: int, max_row: int, max_col: int) -> int:
    col += dx
    row += dy
    while 0 <= row < max_row and 0 <= col < max_col and curr[row][col] == FLOOR:
        col += dx
        row += dy
    if 0 <= row < max_row and 0 <= col < max_col:
        return int(curr[row][col] == OCCUPIED)
    return 0


def solve(grid: List[List[int]], limit: int, counter: Callable) -> int:
    grid1, grid2 = copy.deepcopy(grid), copy.deepcopy(grid)
    while one_iter(grid1, grid2, limit, counter):
        grid1, grid2 = grid2, grid1

    cnt = 0
    for el in chain.from_iterable(grid1):
        cnt += el == OCCUPIED
    return cnt


grid = parse_input(input_reader("inputs/11.txt"))
print(solve(grid, 4, count_near))
print(solve(grid, 5, count_far))

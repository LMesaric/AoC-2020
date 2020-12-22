from collections import deque
from itertools import groupby, islice
from typing import Collection, Deque, Tuple


def input_reader(path: str) -> Tuple[Deque[int], Deque[int]]:
    with open(path) as f:
        lines = [l.rstrip() for l in f.readlines()]
    p1, p2 = [list(g) for k, g in groupby(lines, lambda l: bool(l)) if k]
    p1 = deque(map(int, p1[1:]))
    p2 = deque(map(int, p2[1:]))
    return p1, p2


def calc_score(deck: Collection[int]) -> int:
    multiplier = len(deck)
    score = 0
    for c in deck:
        score += c * multiplier
        multiplier -= 1
    return score


def play_game(p1: Deque[int], p2: Deque[int], recursive: bool) -> bool:
    cache = set()
    while p1 and p2:
        if recursive:
            frozen_state = (tuple(p1), tuple(p2))
            if frozen_state in cache:
                return True
            cache.add(frozen_state)

        c1, c2 = p1.popleft(), p2.popleft()

        if recursive and c1 <= len(p1) and c2 <= len(p2):
            p1_sub, p2_sub = deque(islice(p1, c1)), deque(islice(p2, c2))
            p1_won = play_game(p1_sub, p2_sub, recursive)
        else:
            p1_won = c1 > c2

        if p1_won:
            p1.extend((c1, c2))
        else:
            p2.extend((c2, c1))

    return bool(p1)


def solve_a(p1: Deque[int], p2: Deque[int]) -> int:
    winner = p1 if play_game(p1, p2, False) else p2
    return calc_score(winner)


def solve_b(p1: Deque[int], p2: Deque[int]):
    winner = p1 if play_game(p1, p2, True) else p2
    return calc_score(winner)


deck1, deck2 = input_reader("inputs/22.txt")
print(solve_a(deck1.copy(), deck2.copy()))
print(solve_b(deck1.copy(), deck2.copy()))

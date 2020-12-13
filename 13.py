from math import prod
from typing import List, Tuple

import numpy as np


def input_parser(path: str) -> Tuple[int, List[str]]:
    with open(path) as f:
        line1, line2 = f.readlines()
        return int(line1), line2.strip().split(',')


def clean_departures(deps: List[str]) -> List[Tuple[int, int]]:
    return [(int(t), i) for i, t in enumerate(deps) if t != 'x']


def find_first_bus(deps: List[Tuple[int, int]], start: int) -> Tuple[int, int]:
    t_diff = [(start // d + 1) * d - start for d, _ in deps]
    i = np.argmin(t_diff)
    # noinspection PyTypeChecker
    return deps[i][0], t_diff[i]


def chinese_remainder(n, a):
    sum_, prod_ = 0, prod(n)
    for n_i, a_i in zip(n, a):
        p = prod_ // n_i
        sum_ += a_i * mul_inv(p, n_i) * p
    return sum_ % prod_


def mul_inv(a, b):
    b0, x0, x1 = b, 0, 1
    if b == 1:
        return 1
    while a > 1:
        x0, x1 = x1 - a // b * x0, x0
        a, b = b, a % b
    if x1 < 0:
        x1 += b0
    return x1


def find_earliest_sequence(deps: List[Tuple[int, int]]) -> int:
    max_time = deps[-1][1]
    n = [d0 for d0, _ in deps]
    a = [max_time - d1 for _, d1 in deps]
    return chinese_remainder(n, a) - max_time


start_t, deps_ = input_parser("inputs/13.txt")
deps_ = clean_departures(deps_)

bus_id, wait_t = find_first_bus(deps_, start_t)
print(f'{bus_id} * {wait_t} = {bus_id * wait_t}')

print(find_earliest_sequence(deps_))

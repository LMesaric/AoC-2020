from itertools import groupby
from math import prod

import numpy as np


def input_reader(path: str) -> np.ndarray:
    with open(path) as f:
        return np.array(list(map(int, f)))


def input_cleanup(arr: np.ndarray) -> np.ndarray:
    arr.sort()
    return np.diff(np.concatenate(([0], arr, [arr[-1] + 3])))


def calc_1_3_counts(diff: np.ndarray) -> int:
    return prod(np.unique(diff, return_counts=True)[1])


def count_distinct_ways(diff: np.ndarray) -> int:
    remap = {1: 1, 2: 2, 3: 4, 4: 7}
    return prod([remap[len(tuple(g))] for k, g in groupby(diff, lambda x: x) if k == 1])


clean_input = input_cleanup(input_reader("inputs/10.txt"))
print(calc_1_3_counts(clean_input))
print(count_distinct_ways(clean_input))

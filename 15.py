from itertools import dropwhile
from typing import List


def input_parser(path: str):
    with open(path) as f:
        line = f.read(-1)
        return list(map(int, line.split(',')))


def number_speaker(nums: List[int]):
    memory = {num: i + 1 for i, num in enumerate(nums[:-1])}
    last_spoken = nums[-1]
    curr_i = len(nums)

    while True:
        if last_spoken not in memory:
            next_spoken = 0
        else:
            next_spoken = curr_i - memory[last_spoken]

        memory[last_spoken] = curr_i
        last_spoken = next_spoken
        curr_i += 1
        yield curr_i, last_spoken


def solve(num_gen, nth) -> int:
    return next(dropwhile(lambda i: i[0] < nth, num_gen))[1]


start_nums = input_parser("inputs/15.txt")
print(solve(number_speaker(start_nums), 2020))
print(solve(number_speaker(start_nums), 30000000))

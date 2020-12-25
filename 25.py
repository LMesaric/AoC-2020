from itertools import islice
from typing import Tuple


def input_reader(path: str) -> Tuple[int, int]:
    with open(path) as f:
        card_pub, door_pub = f.readlines()
        return int(card_pub), int(door_pub)


def transform_yield(subject: int):
    value = 1
    while True:
        yield value
        value = (value * subject) % 20201227


def find_loop_size(pub_key: int, subject: int) -> int:
    for loop_size, curr_key in enumerate(transform_yield(subject)):
        if curr_key == pub_key:
            return loop_size


def find_encryption_key(pub_key: int, loop_size: int) -> int:
    key_gen = transform_yield(pub_key)
    return next(islice(key_gen, loop_size, loop_size + 1))


def solve_a(card_pub: int, door_pub: int) -> int:
    card_loop = find_loop_size(card_pub, 7)
    return find_encryption_key(door_pub, card_loop)


def solve_b() -> str:
    return "Courtesy of the Elves :)"


print(solve_a(*input_reader("inputs/25.txt")))
print(solve_b())

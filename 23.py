from itertools import chain, cycle, dropwhile, takewhile
from typing import Iterable, List


def input_reader(path: str) -> List[int]:
    with open(path) as f:
        return list(map(int, list(f.read(-1))))


class SpeedySequentialLinkedList:

    def __init__(self, values: Iterable[int], max_fill_value=0):
        self.first = self.last = 0
        self.min, self.max = min(values), max(values)
        assert self.min == 1

        if max_fill_value > self.max:
            values = chain(values, range(self.max + 1, max_fill_value + 1))
            self.max = max_fill_value

        self.next_node_index: List[int] = [0] * (self.max + 1)
        for v in values:
            self._append(v)

    def _append(self, val: int):
        if self.first <= 0:
            self.first = self.last = val
        else:
            self.next_node_index[self.last] = val
            self.last = val

    def insert_after_value(self, anchor: int, to_insert_first: int, to_insert_last: int):
        if self.last == anchor:
            self.last = to_insert_last
        self.next_node_index[to_insert_last] = self.next_node_index[anchor]
        self.next_node_index[anchor] = to_insert_first

    def rotate_left(self):
        # Assuming there are at least 2 nodes
        first_ = self.first
        self.first = self.next_node_index[first_]
        self.next_node_index[first_] = 0
        self.next_node_index[self.last] = first_
        self.last = first_

    def __iter__(self):
        return SpeedySequentialLinkedListIterator(self)

    def __repr__(self) -> str:
        return str(list(self))


class SpeedySequentialLinkedListIterator:

    def __init__(self, ssll: SpeedySequentialLinkedList):
        self._ssll = ssll
        self._curr = self._ssll.first

    def __next__(self):
        if self._curr <= 0:
            raise StopIteration
        result = self._curr
        self._curr = self._ssll.next_node_index[self._curr]
        return result


def perform_iterations(cups: Iterable[int], n_iter, max_fill_value=0) -> SpeedySequentialLinkedList:
    ssll = SpeedySequentialLinkedList(cups, max_fill_value)
    min_, max_ = ssll.min, ssll.max
    next_map = ssll.next_node_index

    for _ in range(n_iter):
        curr = ssll.first
        left = next_map[curr]
        mid = next_map[left]
        right = next_map[mid]

        next_map[curr] = next_map[right]

        next_val = curr - 1
        while next_val == left or next_val == mid or next_val == right:
            next_val -= 1
        if next_val < min_:
            next_val = max_
        while next_val == left or next_val == mid or next_val == right:
            next_val -= 1

        ssll.insert_after_value(next_val, left, right)
        ssll.rotate_left()

    return ssll


def solve_a(cups: Iterable[int]) -> str:
    ssll = perform_iterations(cups, n_iter=100)
    ssll_cycle = dropwhile(lambda x: x != 1, cycle(ssll))
    next(ssll_cycle)
    result = [i for i in takewhile(lambda x: x != 1, ssll_cycle)]
    return ''.join(str(i) for i in result)


def solve_b(cups: Iterable[int]) -> int:
    ssll = perform_iterations(cups, n_iter=10_000_000, max_fill_value=1_000_000)
    right = ssll.next_node_index[1]
    return right * ssll.next_node_index[right]


data = input_reader("inputs/23.txt")
print(solve_a(data))
print(solve_b(data))

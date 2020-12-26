from functools import reduce
from itertools import chain, groupby
from operator import and_


def group_generator(path):
    with open(path) as f:
        lines = [x.rstrip() for x in f]
    return [list(g) for k, g in groupby(lines, lambda l: bool(l)) if k]


count_any_per_group = lambda group: len(set(chain.from_iterable(group)))
count_all_per_group = lambda group: len(reduce(and_, [set(g) for g in group]))

data = group_generator("inputs/06.txt")
print(sum(count_any_per_group(group) for group in data))
print(sum(count_all_per_group(group) for group in data))

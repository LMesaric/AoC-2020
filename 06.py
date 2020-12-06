from itertools import chain


def group_generator(path):
    with open(path) as f:
        data = [x.strip() for x in f]
        data.append('')

    curr_group = []
    for line in data:
        if not line:
            yield curr_group
            curr_group = []
        else:
            curr_group.append(line)


count_any_per_group = lambda group: len(set(chain.from_iterable(group)))


def count_all_per_group(group):
    group_iter = iter(group)
    q_set = set(next(group_iter))
    for answ in group_iter:
        q_set.intersection_update(answ)
    return len(q_set)


print(sum(count_any_per_group(group) for group in group_generator("inputs/6.txt")))
print(sum(count_all_per_group(group) for group in group_generator("inputs/6.txt")))

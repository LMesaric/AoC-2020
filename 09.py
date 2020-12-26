from collections import deque
from itertools import islice


def input_generator(path):
    with open(path) as f:
        for line in f:
            yield int(line)


def checker(input_gen, preamble=25):
    queue = deque(islice(input_gen, preamble))
    curr_set = set(queue)

    for num in input_gen:
        if not find_two_different(num, curr_set):
            return num
        curr_set.remove(queue.popleft())
        curr_set.add(num)
        queue.append(num)


def find_two_different(wanted_sum, data):
    for num in data:
        if num * 2 == wanted_sum:
            continue
        if wanted_sum - num in data:
            return True
    return False


def find_contiguous_range(wanted_sum, data_stream):
    curr_sum = 0
    queue = deque()

    while curr_sum != wanted_sum:
        while curr_sum < wanted_sum:
            try:
                num = next(data_stream)
            except StopIteration:
                return None
            queue.append(num)
            curr_sum += num

        while curr_sum > wanted_sum:
            curr_sum -= queue.popleft()

    return queue


invalid_sum = checker(input_generator("inputs/09.txt"))
print(invalid_sum)

found_range = find_contiguous_range(invalid_sum, input_generator("inputs/09.txt"))
print(min(found_range) + max(found_range))

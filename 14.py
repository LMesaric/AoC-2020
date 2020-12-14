from itertools import product


def input_parser(path: str):
    with open(path) as f:
        for line in f:
            left, right = line.strip().split(' = ')
            if left == "mask":
                yield "mask", -1, right
            else:
                pos = int(left[4:-1])
                yield "mem", pos, int(right)


def solve_a(input_gen) -> int:
    curr_mask_0 = curr_mask_1 = 0
    memory = dict()
    for key, pos, right in input_gen:
        if key == "mask":
            curr_mask_0 = int(right.replace('X', '1'), base=2)
            curr_mask_1 = int(right.replace('X', '0'), base=2)
        else:
            memory[pos] = right & curr_mask_0 | curr_mask_1
    return sum(memory.values())


def masks_generator(raw_mask: str):
    for x_replacement in product('01', repeat=raw_mask.count('X')):
        mask = raw_mask
        for bit in x_replacement:
            mask = mask.replace('X', bit, 1)
        yield int(mask, base=2)


def solve_b(input_gen) -> int:
    curr_mask_clean_X, curr_masks_or = 0, None
    memory = dict()
    for key, pos, right in input_gen:
        if key == "mask":
            curr_mask_clean_X = int(right.replace('0', '1').replace('X', '0'), base=2)
            curr_masks_or = list(masks_generator(right))
        else:
            pos &= curr_mask_clean_X
            for mask in curr_masks_or:
                memory[pos | mask] = right
            pass
    return sum(memory.values())


print(solve_a(input_parser("inputs/14.txt")))
print(solve_b(input_parser("inputs/14.txt")))

with open("inputs/1.txt") as f:
    data = set(map(int, f.readlines()))


def find_two(total):
    for num in data:
        if total - num in data:
            return num * (total - num)
    return None


def find_three(total):
    for num in data:
        prod = find_two(total - num)
        if prod is not None:
            return num * prod


print(find_two(2020))
print(find_three(2020))

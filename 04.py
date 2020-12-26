from itertools import groupby


def input_reader(path):
    with open(path) as f:
        lines = [x.rstrip() for x in f]
    groups = [list(g) for k, g in groupby(lines, lambda l: bool(l)) if k]
    return [' '.join(l) for l in groups]


def validate_num_range(num, cnt, low, high):
    if len(num) != cnt:
        return False
    return low <= int(num) <= high


def validate_year(year, low, high):
    return validate_num_range(year, 4, low, high)


def validate_hgt(hgt):
    if hgt.endswith("cm"):
        return validate_num_range(hgt[:-2], 3, 150, 193)
    if hgt.endswith("in"):
        return validate_num_range(hgt[:-2], 2, 59, 76)


def validate_hcl(hcl):
    if not hcl.startswith('#'):
        return False
    hcl = hcl[1:]
    if len(hcl) != 6 or hcl != hcl.lower():
        return False
    _ = int(hcl, base=16)
    return True


def validate_ecl(ecl):
    return ecl in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')


def validate_pid(pid):
    if len(pid) != 9:
        return False
    for char in pid:
        if ord(char) not in range(ord('0'), ord('9') + 1):
            return False
    return True


def validate_pass(psprt):
    return all((
        validate_year(psprt['byr'], 1920, 2002),
        validate_year(psprt['iyr'], 2010, 2020),
        validate_year(psprt['eyr'], 2020, 2030),
        validate_hgt(psprt['hgt']),
        validate_hcl(psprt['hcl']),
        validate_ecl(psprt['ecl']),
        validate_pid(psprt['pid'])
    ))


mandatory = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
cnt_a = cnt_b = 0

data = input_reader("inputs/04.txt")
for raw_passport in data:
    fields = dict(field.split(':') for field in raw_passport.split())
    if mandatory.issubset(fields) and len(fields) in (7, 8):
        cnt_a += 1
        if validate_pass(fields):
            cnt_b += 1

print(cnt_a)
print(cnt_b)

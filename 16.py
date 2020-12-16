from itertools import groupby
from typing import List


def input_parser(path: str):
    with open(path) as f:
        lines = [l.strip() for l in f.readlines()]
        filtered = [list(g) for k, g in groupby(lines, lambda l: bool(l)) if k]
        constraints = dict()
        for c in filtered[0]:
            range_name, v = c.split(': ')
            left, right = v.split(' or ')
            left = left.split('-')
            right = right.split('-')
            constraints[range_name] = (range(int(left[0]), int(left[1]) + 1),
                                       range(int(right[0]), int(right[1]) + 1))
        return constraints, parse_ticket(filtered[1][1]), list(map(parse_ticket, filtered[2][1:]))


def parse_ticket(ticket: str) -> List[int]:
    return list(map(int, ticket.split(',')))


def solve_a(ranges, tickets):
    sum_, valid_tickets = 0, []
    for ticket in tickets:
        for field in ticket:
            for r1, r2 in ranges.values():
                if field in r1 or field in r2:
                    break
            else:
                sum_ += field
                break
        else:
            valid_tickets.append(ticket)
    return sum_, valid_tickets


def determine_field_order(ranges, tickets):
    valids = {k: [False] * len(ranges) for k in ranges}
    for range_name, (r1, r2) in ranges.items():
        for field_idx in range(len(ranges)):
            for ticket in tickets:
                if ticket[field_idx] not in r1 and ticket[field_idx] not in r2:
                    break
            else:
                valids[range_name][field_idx] = True

    valids_sorted = sorted(valids.items(), key=lambda v: v[1].count(True))
    field_indices = dict()
    for field_name, possible_positions in valids_sorted:
        assert possible_positions.count(True) == 1
        idx = possible_positions.index(True)
        field_indices[field_name] = idx
        for _, v in valids_sorted:
            v[idx] = False
    return field_indices


def solve_b(ranges, tickets, my_ticket):
    field_indices = determine_field_order(ranges, tickets)
    prod = 1
    for k, v in field_indices.items():
        if k.startswith('departure'):
            prod *= my_ticket[v]
    return prod


data = input_parser("inputs/16.txt")
sum_, valid_tickets = solve_a(data[0], data[2])
print(sum_)
print(solve_b(data[0], valid_tickets, data[1]))

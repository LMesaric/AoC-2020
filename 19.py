import re
from itertools import groupby
from typing import Any, Dict, List, Tuple


def input_reader(path: str) -> Tuple[List[str], List[str]]:
    with open(path) as f:
        lines = [l.rstrip() for l in f.readlines()]
    rules, messages = [list(g) for k, g in groupby(lines, lambda l: bool(l)) if k]
    return rules, messages


def input_parser(rules: List[str]) -> Dict[int, int]:
    def parse_rule_part(part: str) -> List[int]:
        return list(map(int, part.split()))

    rules_map = dict()
    for rule in rules:
        id_, raw = rule.split(': ')
        id_ = int(id_)
        if raw[0] == '"':
            rules_map[id_] = raw[1:-1]
        elif '|' in raw:
            raw_1, raw_2 = raw.split(' | ')
            rules_map[id_] = (parse_rule_part(raw_1), parse_rule_part(raw_2))
        else:
            rules_map[id_] = parse_rule_part(raw)
    return rules_map


def build_regex_part(indices: List[int], rules: Dict[int, Any], dp: Dict[int, str], override_8_11):
    return ''.join(build_regex(rules, dp, i, override_8_11) for i in indices)


def build_regex(rules: Dict[int, Any], dp: Dict[int, str], idx: int, override_8_11):
    if idx in dp:
        return dp[idx]

    curr = rules[idx]
    if override_8_11 and idx == 8:
        dp[idx] = f'(?:{build_regex_part(curr, rules, dp, override_8_11)})+'
    elif override_8_11 and idx == 11:
        r1 = build_regex(rules, dp, 42, override_8_11)
        r2 = build_regex(rules, dp, 31, override_8_11)
        dp[idx] = f'(?:(?:{r1}{r2})|(?:{r1 * 2}{r2 * 2})|(?:{r1 * 3}{r2 * 3})|' \
                  f'(?:{r1 * 4}{r2 * 4})|(?:{r1 * 5}{r2 * 5}))'
    elif isinstance(curr, str):
        dp[idx] = curr
    elif isinstance(curr, list):
        dp[idx] = build_regex_part(curr, rules, dp, override_8_11)
    else:  # tuple
        dp[idx] = f'(?:{build_regex_part(curr[0], rules, dp, override_8_11)}|' \
                  f'{build_regex_part(curr[1], rules, dp, override_8_11)})'
    return dp[idx]


def count_full_matches(messages: List[str], regex: str) -> int:
    cnt = 0
    for m in messages:
        cnt += re.fullmatch(regex, m) is not None
    return cnt


rules_, messages_ = input_reader("inputs/19.txt")
rules_ = input_parser(rules_)

print(count_full_matches(messages_, build_regex(rules_, dict(), 0, False)))
print(count_full_matches(messages_, build_regex(rules_, dict(), 0, True)))

from collections import defaultdict
from functools import reduce
from operator import and_, or_
from typing import Dict, List, Set, Tuple


def input_reader(path: str) -> List[Tuple[List[str], List[str]]]:
    with open(path) as f:
        lines = [l.rstrip(')\r\n').split(' (contains ') for l in f.readlines()]
    parsed = []
    for ingredients_raw, allergens_raw in lines:
        parsed.append((ingredients_raw.split(' '), allergens_raw.split(', ')))
    return parsed


def solve_a(data: List[Tuple[List[str], List[str]]]) -> Tuple[int, Dict[str, Set[str]]]:
    allergens_to_ingredients: Dict[str, List[Set[str]]] = defaultdict(list)
    for ingredients, allergens in data:
        for allergen in allergens:
            allergens_to_ingredients[allergen].append(set(ingredients))

    allergenic_ingredients = {allergen: reduce(and_, ingredients)
                              for allergen, ingredients in allergens_to_ingredients.items()}

    all_allergenic_ingredients = reduce(or_, allergenic_ingredients.values())

    cnt_inert = 0
    for ings, _ in data:
        for ing in ings:
            cnt_inert += ing not in all_allergenic_ingredients

    return cnt_inert, allergenic_ingredients


def solve_b(allergenic_ingredients: Dict[str, Set[str]]) -> str:
    final_mapping: Dict[str, str] = dict()
    while allergenic_ingredients:
        for allergen, possible_ingredients in allergenic_ingredients.items():
            if len(possible_ingredients) == 1:
                break
        # noinspection PyUnboundLocalVariable
        final_mapping[allergen] = next(iter(possible_ingredients))

        del allergenic_ingredients[allergen]
        for v in allergenic_ingredients.values():
            v.discard(final_mapping[allergen])

    return ','.join([ingredient for _, ingredient in sorted(final_mapping.items())])


cnt, mapping = solve_a(input_reader("inputs/21.txt"))
print(cnt)
print(solve_b(mapping))

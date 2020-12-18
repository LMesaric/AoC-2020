import re
from collections import deque
from dataclasses import dataclass
from typing import List, Union


def input_reader(path: str) -> List[str]:
    with open(path) as f:
        return f.readlines()


def input_parser(data: List[str]):
    for line in data:
        parts = line.replace('(', '( ').replace(')', ' )').split()
        for i in range(len(parts)):
            if parts[i] not in '+*()':
                parts[i] = int(parts[i])
        yield parts


def eval_equal_precedence(expr: List[Union[int, str]]) -> int:
    expr = deque(expr)
    stack = []
    while expr:
        val = expr.popleft()
        if isinstance(val, int):
            if not stack or stack[-1] == '(':
                stack.append(val)
            else:
                oper = stack.pop()
                prev = stack.pop()
                if oper == '+':
                    new = prev + val
                else:
                    new = prev * val
                stack.append(new)
        elif val == ')':
            inner_res = stack.pop()
            assert stack.pop() == '('
            expr.appendleft(inner_res)
        else:  # val in '+*('
            stack.append(val)

    res = stack.pop()
    assert len(stack) == 0
    return res


@dataclass
class MyBrokenInt:
    v: int

    def __add__(self, other):
        return MyBrokenInt(self.v * other.v)

    def __mul__(self, other):
        return MyBrokenInt(self.v + other.v)


def eval_inverse_precedence(eq: str) -> int:
    eq = eq.strip().translate(str.maketrans({'+': '*', '*': '+'}))
    return eval(re.sub(r'(\d+)', r'MyBrokenInt(\1)', eq)).v


def solve_a(expr_gen) -> int:
    return sum(eval_equal_precedence(expr) for expr in expr_gen)


def solve_b(data: List[str]) -> int:
    return sum(eval_inverse_precedence(expr) for expr in data)


data = input_reader("inputs/18.txt")
print(solve_a(input_parser(data)))
print(solve_b(data))

from collections import defaultdict, namedtuple

NameCntPair = namedtuple("NameCntPair", ["name", "cnt"])


def rule_generator(path):
    with open(path) as f:
        for line in f:
            yield line_parse(line.strip().rstrip('.'))


def line_parse(line):
    parent, children_raw = line.split(" bags contain ")
    if children_raw == "no other bags":
        return parent, []
    return parent, list(children_parser(children_raw.split(', ')))


def children_parser(children):
    for child in children:
        num, rest = child.split(' ', 1)
        name = rest.rsplit(' ', 1)[0]
        yield NameCntPair(name, int(num))


def build_graph_reverse(rules):
    graph = defaultdict(list)
    for parent, children in rules:
        for child in children:
            graph[child.name].append(NameCntPair(parent, child.cnt))
    return graph


def build_graph(rules):
    return dict(rules)


def unique_bags(graph, start, bags):
    children = graph[start]
    if not children:
        return
    for c in children:
        if c.name in bags:
            continue
        bags.add(c.name)
        unique_bags(graph, c.name, bags)


def count_bags_inside(graph, start, dp):
    children = graph[start]
    if not children:
        return 0

    sum_ = 0
    for c in children:
        if c.name not in dp:
            dp[c.name] = count_bags_inside(graph, c.name, dp)
        sum_ += (dp[c.name] + 1) * c.cnt
    return sum_


set_ = set()
unique_bags(
    build_graph_reverse(rule_generator("inputs/7.txt")),
    "shiny gold",
    set_
)
print(len(set_))

print(count_bags_inside(
    build_graph(rule_generator("inputs/7.txt")),
    "shiny gold",
    dict()
))

from itertools import groupby
from math import sqrt
from typing import Dict, List, Set

Tile = List[str]


def input_reader(path: str) -> Dict[int, Tile]:
    with open(path) as f:
        lines = [l.rstrip() for l in f.readlines()]
    raw_tiles = [list(g) for k, g in groupby(lines, lambda l: bool(l)) if k]
    return {int(tile[0][5:-1]): tile[1:] for tile in raw_tiles}


def get_tile_edges(tile: Tile) -> Dict[str, str]:
    top = tile[0]
    bottom = tile[-1]
    left = ''.join([r[0] for r in tile])
    right = ''.join([r[-1] for r in tile])
    return {'t': top,
            'tr': top[::-1],
            'b': bottom,
            'br': bottom[::-1],
            'l': left,
            'lr': left[::-1],
            'r': right,
            'rr': right[::-1]}


def find_corners(tile_map: Dict[int, Tile]):
    all_borders: Dict[int, Dict[str, str]] = {k: get_tile_edges(v) for k, v in tile_map.items()}

    def all_borders_except_one(tile_id_skip: int) -> Set[str]:
        others_ = set()
        for tile_id_ in all_borders:
            if tile_id_ != tile_id_skip:
                others_.update(all_borders[tile_id_].values())
        return others_

    for tile_id, borders in all_borders.items():
        others = all_borders_except_one(tile_id)
        single_sides = set()
        for k, v in borders.items():
            if v not in others:
                single_sides.add(k)

        assert len(single_sides) <= 4
        if len(single_sides) == 4:
            yield tile_id, single_sides


def solve_a(tile_map: Dict[int, Tile]) -> int:
    prod = 1
    for tile_id, _ in find_corners(tile_map):
        prod *= tile_id
    return prod


def flip_tile_reverse_rows(tile: Tile) -> Tile:
    return tile[::-1]


def flip_tile_reverse_cols(tile: Tile) -> Tile:
    for i in range(len(tile)):
        tile[i] = tile[i][::-1]
    return tile


def rotate_tile_right(tile: Tile) -> Tile:
    n = len(tile)
    new_tile_raw = [[''] * n for _ in range(n)]
    for y in range(n):
        for x in range(n):
            new_tile_raw[x][n - 1 - y] = tile[y][x]
    return [''.join(row) for row in new_tile_raw]


def transform_tile_to_fit(tile: Tile, curr_pos: str, req_pos: str) -> Tile:
    assert req_pos in ('t', 'l')

    if req_pos == 'l':
        return flip_tile_reverse_cols(rotate_tile_right(transform_tile_to_fit(tile, curr_pos, 't')))

    if curr_pos == 't':
        return tile
    elif curr_pos == 'tr':
        return flip_tile_reverse_cols(tile)
    elif curr_pos == 'l':
        return transform_tile_to_fit(flip_tile_reverse_rows(tile), 'lr', req_pos)
    elif curr_pos == 'lr':
        return rotate_tile_right(tile)
    elif curr_pos == 'b':
        return flip_tile_reverse_rows(tile)
    elif curr_pos == 'br':
        return transform_tile_to_fit(flip_tile_reverse_cols(tile), 'b', req_pos)
    elif curr_pos == 'r':
        return transform_tile_to_fit(rotate_tile_right(tile), 'br', req_pos)
    elif curr_pos == 'rr':
        return transform_tile_to_fit(rotate_tile_right(tile), 'b', req_pos)
    else:
        assert False


def merge_tiles_row(tile_map: Dict[int, Tile], positions: List[int]) -> List[str]:
    merged = []
    for composite_row in zip(*[tile_map[i] for i in positions]):
        merged.append(''.join([tile_row[1:-1] for tile_row in composite_row]))
    return merged


def merge_tiles(tile_map: Dict[int, Tile], positions: List[List[int]]) -> Tile:
    for tile in tile_map.values():
        del tile[0]
        del tile[-1]

    merged = []
    for row in positions:
        merged.extend(merge_tiles_row(tile_map, row))
    return merged


def prepare_top_left_corner(tile_map: Dict[int, Tile]) -> int:
    for corner_tile_id, single_borders in find_corners(tile_map):
        break

    if 'b' in single_borders:
        assert 'br' in single_borders and 't' not in single_borders
        tile_map[corner_tile_id] = flip_tile_reverse_rows(tile_map[corner_tile_id])

    if 'r' in single_borders:
        assert 'rr' in single_borders and 'l' not in single_borders
        tile_map[corner_tile_id] = flip_tile_reverse_cols(tile_map[corner_tile_id])

    return corner_tile_id


def find_common_borders(tile_1: Dict[str, str], tile_2: Dict[str, str]) -> Dict[str, str]:
    res = dict()
    tile_2_inverse = {v: k for k, v in tile_2.items()}
    for k, v in tile_1.items():
        if v in tile_2_inverse:
            res[k] = tile_2_inverse[v]
    return res


def find_exact_order(tile_map: Dict[int, Tile]) -> List[List[int]]:
    n = int(sqrt(len(tile_map)))
    final_positions = [[-1] * n for _ in range(n)]
    final_positions[0][0] = prepare_top_left_corner(tile_map)

    all_borders: Dict[int, Dict[str, str]] = {k: get_tile_edges(v) for k, v in tile_map.items()}
    unused_tiles = set(tile_map) - {final_positions[0][0]}

    def find_and_fit_child(y, x, dy, dx, parent_side, child_side):
        for tile_id in unused_tiles:
            parent_id = final_positions[y - dy][x - dx]
            commons = find_common_borders(all_borders[parent_id], all_borders[tile_id])
            if not commons or tile_id == parent_id or parent_side not in commons:
                continue

            tile_map[tile_id] = transform_tile_to_fit(tile_map[tile_id], commons[parent_side], child_side)
            all_borders[tile_id] = get_tile_edges(tile_map[tile_id])
            final_positions[y][x] = tile_id
            unused_tiles.remove(tile_id)
            break

    for x in range(n):
        for y in range(n):
            if x == y == 0:
                continue
            elif y == 0:
                find_and_fit_child(y, x, 0, 1, 'r', 'l')
            else:
                find_and_fit_child(y, x, 1, 0, 'b', 't')

    return final_positions


def find_monsters(tile: Tile):
    deltas = ((1, 0), (2, 1), (2, 4), (1, 5), (1, 6), (2, 7), (2, 10), (1, 11),
              (1, 12), (2, 13), (2, 16), (1, 17), (0, 18), (1, 18), (1, 19))

    for y in range(len(tile) - 2):
        for x in range(len(tile) - 19):
            if all(tile[y + dy][x + dx] == '#' for dy, dx in deltas):
                yield y, x


def solve_b(tile_map: Dict[int, Tile]) -> int:
    final_positions = find_exact_order(tile_map)
    merged_tile = merge_tiles(tile_map, final_positions)

    for k in ('t', 'tr', 'l', 'lr', 'r', 'rr', 'b', 'br'):
        found_positions = list(find_monsters(transform_tile_to_fit(merged_tile.copy(), k, 't')))
        if found_positions:
            break

    total_waves = 0
    for row in merged_tile:
        total_waves += row.count('#')

    return total_waves - len(found_positions) * 15


tile_map_ = input_reader("inputs/20.txt")
print(solve_a(tile_map_))
print(solve_b(tile_map_))

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Boat:
    facing: int = 0  # E = 0, N = 90, W = 180, S = 270
    position_x: int = 0
    position_y: int = 0

    def manhattan(self):
        return abs(self.position_x) + abs(self.position_y)


@dataclass
class Waypoint(Boat):
    waypoint_offset_x: int = 10
    waypoint_offset_y: int = 1


def input_reader(path: str) -> List[str]:
    with open(path) as f:
        return f.readlines()


def parse_line(line: str) -> Tuple[str, int]:
    d = line[0]
    v = int(line[1:])

    if d == 'S':
        d = 'N'
        v *= -1
    elif d == 'W':
        d = 'E'
        v *= -1
    elif d == 'R':
        d = 'L'
        v = 360 - v

    return d, v


def move_boat(boat: Boat, d: str, v: int):
    if d == 'N':
        boat.position_y += v
    elif d == 'E':
        boat.position_x += v
    elif d == 'L':
        boat.facing = (boat.facing + v) % 360
    elif d == 'F':
        if boat.facing == 0:
            boat.position_x += v
        elif boat.facing == 90:
            boat.position_y += v
        elif boat.facing == 180:
            boat.position_x -= v
        elif boat.facing == 270:
            boat.position_y -= v


def move_waypoint(waypoint: Waypoint, d: str, v: int):
    if d == 'N':
        waypoint.waypoint_offset_y += v
    elif d == 'E':
        waypoint.waypoint_offset_x += v
    elif d == 'L':
        if v == 90:
            waypoint.waypoint_offset_x, waypoint.waypoint_offset_y = -waypoint.waypoint_offset_y, waypoint.waypoint_offset_x
        elif v == 180:
            waypoint.waypoint_offset_x *= -1
            waypoint.waypoint_offset_y *= -1
        elif v == 270:
            waypoint.waypoint_offset_x, waypoint.waypoint_offset_y = waypoint.waypoint_offset_y, -waypoint.waypoint_offset_x
    elif d == 'F':
        waypoint.position_x += waypoint.waypoint_offset_x * v
        waypoint.position_y += waypoint.waypoint_offset_y * v


data = list(map(parse_line, input_reader("inputs/12.txt")))

b = Boat()
for d, v in data:
    move_boat(b, d, v)
print(b.manhattan())

w = Waypoint()
for d, v in data:
    move_waypoint(w, d, v)
print(w.manhattan())

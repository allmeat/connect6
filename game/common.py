from typing import NamedTuple


def repr_direction(dir_func):
    dx, dy = dir_func(0, 0)  # differentiate
    return '({}, {})'.format(dy, dx)


class Point(NamedTuple):
    x: int
    y: int


class Coord(NamedTuple):
    x_axis: [0]*19
    y_axis: [0]*19

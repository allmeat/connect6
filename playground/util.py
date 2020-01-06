import os
from typing import List
from board import Stone


def turn_check(log: List[Stone], each_move: int, first_move: int) -> str:
    if (len(log) - first_move) % (2 * each_move) in list(range(0, each_move)):
        return "w"
    return "b"


def exit_by_alias(_: List[Stone]):
    print("wrong player name")
    os.sys.exit()


class Direction:

    HORIZONTAL = "h"
    VERTICAL = "v"
    NEGATIVE_DIAGONAL = "nd"
    POSITIVE_DIAGONAL = "pd"

    UP = "u"
    DOWN = "d"
    LEFT = "l"
    RIGHT = "r"
    UP_LEFT = "ul"
    UP_RIGHT = "ur"
    DOWN_LEFT = "dl"
    DOWN_RIGHT = "dr"
    ALL_DIRECTIONS = [
        UP,
        DOWN,
        LEFT,
        RIGHT,
        UP_LEFT,
        UP_RIGHT,
        DOWN_LEFT,
        DOWN_RIGHT,
    ]

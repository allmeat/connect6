from typing import List
from board import Stone
import numpy as np
from board import BoardConfig

def turn_check(log: List[Stone], each_move: int, first_move: int) -> str:
    if (len(log) - first_move) % (2 * each_move) in list(range(0, each_move)):
        return "w"
    return "b"


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



class BoardInterpreter:

    def __init__(self, board_config: BoardConfig):
        self.k = board_config.connect
        self.m = board_config.row
        self.n = board_config.column
        self.p = board_config.each_move
        self.q = board_config.first_move

    def array_to_board(self, x: int) -> str:
        if x == 0:
            points = "+"
        elif x == 1:
            points = "B"
        elif x == 2:
            points = "W"
        else:  # x == -1:
            points = "S"
        return points

    def stone_to_array(self, log: List[Stone]) -> np.array:
        stone_array = np.zeros((self.m, self.n))
        for pos in log:
            x = int(pos.x) - 1
            y = int(pos.y) - 1
            if pos.color == "b":
                stone_array[y, x] = 1
            elif pos.color == "w":
                stone_array[y, x] = 2
            elif pos.color == "s":
                stone_array[y, x] = -1
        return stone_array

    def array_to_stone(self, stone_array: np.array, color: str) -> List[Stone]:
        if color == "b":
            out = 1
        elif color == "w":
            out = 2
        else:
            out = -1
        y, x = np.where(stone_array == out)
        positions = list(zip(list(x), list(y)))
        stones = [Stone(str(x + 1), str(y + 1), color) for x, y in positions]
        return stones

    def draw_board(self, log: List[Stone]):
        stone_array = self.stone_to_array(log)
        join_column = list(map(lambda y: " ".join([self.array_to_board(x) for i, x in enumerate(y)]), stone_array))
        join_row = "\n" + "\n".join(join_column)
        print(join_row)

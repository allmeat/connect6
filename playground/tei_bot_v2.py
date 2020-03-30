import numpy as np
from random import randint, choice
from typing import List
from board import Stone, BoardConfig, BoardInterpreter
from util import turn_check, Direction

from tei_bot_v2_util import get_black, get_white, find_connected_19x19, suggest_position_by_connected_element

class TeiBot:

    def __init__(self, board_config: BoardConfig):
        self.k = board_config.connect
        self.m = board_config.row
        self.n = board_config.column
        self.p = board_config.each_move
        self.q = board_config.first_move
        self.boardInterpreter = BoardInterpreter(board_config)

    # array_to_board = lambda self, x: self.boardInterpreter.array_to_board(x)

    def array_to_board(self, x: int) -> str:
        return self.boardInterpreter.array_to_board(x)

    def stone_to_array(self, log: List[Stone]) -> np.array:
        return self.boardInterpreter.stone_to_array(log)

    def array_to_stone(self, stone_array: np.array, color: str) -> List[Stone]:
        return self.boardInterpreter.array_to_stone(stone_array, color)

    def draw_board(self, log: List[Stone]):
        self.boardInterpreter.draw_board(log)


    def suggest_positions(self, log: List[Stone], lower: int = 1, upper: int = 19) -> List[Stone]:
        turn = turn_check(log, self.p, self.q)
        """
        lastLogNum = len(log)- 1
        lastLogNum_1 = len(log) - 2
        turn_0 = log[lastLogNum].color
        turn_1 = log[lastLogNum_1].color
        if turn_0 == "b":
            if turn_1=="b":
                turn = "w"
            else:
                turn="b"
        else:
            if turn_1 == "b":
                turn = "b"
            else:
                turn = "w"

        """

        stone_array = self.stone_to_array(log)
        suggestions = suggest_position_by_connected_element(stone_array, turn) * -1
        suggestions = np.clip(stone_array + suggestions, -1, 0)
        suggestions = self.array_to_stone(suggestions, "s")
        return suggestions

    def put_stone(self, log: List[Stone]) -> Stone:
        turn = turn_check(log, self.p, self.q)
        if len(log) == 0:
            x = randint(1, self.n)
            y = randint(1, self.m)
            return Stone(str(x), str(y), turn)
        elif len(self.suggest_positions(log))>0:
            position = choice(self.suggest_positions(log))
        else:
            x = randint(1, self.n)
            y = randint(1, self.m)
            return Stone(str(x), str(y), turn)
        return Stone(position.x, position.y, turn)


if __name__ == "__main__":
    diagonal_test_log = [
        Stone("1", "2", "b"),
        Stone("1", "1", "w"),
        Stone("2", "2", "w"),
        Stone("1", "3", "b"),
        Stone("1", "4", "b"),
        Stone("3", "3", "w"),
        Stone("4", "4", "w"),
        Stone("1", "5", "b"),
        Stone("1", "6", "b"),
        Stone("5", "5", "w"),
        Stone("7", "5", "w"),
        Stone("10", "11", "b"),
        Stone("11", "11", "b"),
        Stone("6", "6", "w"),
    ]

    a = np.array(
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 1, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    )

    black = get_black(a)
    white = get_white(a)

    bb = np.where(black == 1)
    ww = np.where(white == 1)
    bb = list(zip(bb[0], bb[1]))
    ww = list(zip(ww[0], ww[1]))
    bbstone = [Stone(x[1]+1, x[0]+1, "b") for x in bb]
    wwstone = [Stone(x[1]+1, x[0]+1, "w") for x in ww]
    bbstone.extend(wwstone)



    config = BoardConfig(19, 19, 6, 2, 1)
    tei_bot = TeiBot(config)
    tei_bot.draw_board(bbstone)

    suggest_positions = tei_bot.suggest_positions(bbstone)
    tei_bot.draw_board(suggest_positions)

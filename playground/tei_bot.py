import numpy as np
from random import randint, choice
from typing import List
from board import Stone, BoardConfig
from util import turn_check, Direction
from util import BoardInterpreter

class TeiBot:

    def __init__(self, board_config: BoardConfig):
        self.k = board_config.connect
        self.m = board_config.row
        self.n = board_config.column
        self.p = board_config.each_move
        self.q = board_config.first_move
        self.boardInterpreter = BoardInterpreter(board_config)


    #array_to_board = lambda self, x: self.boardInterpreter.array_to_board(x)

    def array_to_board(self, x: int) -> str:
        return self.boardInterpreter.array_to_board(x)

    def stone_to_array(self, log: List[Stone]) -> np.array:
        return self.boardInterpreter.stone_to_array(log)

    def array_to_stone(self, stone_array: np.array, color: str) -> List[Stone]:
        return self.boardInterpreter.array_to_stone(stone_array, color)

    def draw_board(self, log: List[Stone]):
        self.boardInterpreter.draw_board(log)
    '''
    @staticmethod
    def array_to_board(x: int) -> str:
        if x == 0:
            points = "+"
        elif x == 1:
            points = "B"
        elif x == 2:
            points = "W"
        else:  # x == -1:
            points = "S"
        return points

    @staticmethod
    def stone_to_array(log: List[Stone]) -> np.array:
        stone_array = np.zeros((19, 19))
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

    @staticmethod
    def array_to_stone(stone_array: np.array, color: str) -> List[Stone]:
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
    '''
    '''
    def draw_board(self, log: List[Stone]):
        stone_array = self.stone_to_array(log)
        join_column = list(map(lambda y: " ".join([self.array_to_board(x) for i, x in enumerate(y)]), stone_array))
        join_row = "\n" + "\n".join(join_column)
        print(join_row)
    '''


    @staticmethod
    def move_stone(stone: Stone, direction: str, stride: int = 1) -> Stone:
        x = int(stone.x)
        y = int(stone.y)

        if direction == Direction.LEFT:
            x = x - stride
        elif direction == Direction.RIGHT:
            x = x + stride
        elif direction == Direction.UP:
            y = y - stride
        elif direction == Direction.DOWN:
            y = y + stride
        elif direction == Direction.UP_LEFT:
            y = y - stride
            x = x - stride
        elif direction == Direction.UP_RIGHT:
            y = y - stride
            x = x + stride
        elif direction == Direction.DOWN_LEFT:
            y = y + stride
            x = x - stride
        else:  # direction == Direction.DOWN_RIGHT:
            y = y + stride
            x = x + stride
        return Stone(str(x), str(y), stone.color)

    def suggest_positions(self, log: List[Stone], lower: int = 1, upper: int = 19) -> List[Stone]:
        suggestions = []
        for d in Direction.ALL_DIRECTIONS:
            position = list(map(lambda x: self.move_stone(x, d, 1), log))
            position = list(filter(lambda x: lower <= int(x.x) <= upper and lower <= int(x.y) <= upper, position))
            suggestions = suggestions + position

        suggestions = set(map(lambda x: x.x + " " + x.y, suggestions))
        suggestions = list(map(lambda x: x.split(" "), suggestions))
        suggestions = list(map(lambda z: Stone(z[0], z[1], "s"), suggestions))
        stone_array = self.stone_to_array(log)
        suggestions = self.stone_to_array(suggestions)
        suggestions = np.clip(stone_array + suggestions, -1, 0)
        suggestions = self.array_to_stone(suggestions, "s")
        return suggestions

    def put_stone(self, log: List[Stone]) -> Stone:
        turn = turn_check(log, self.p, self.q)
        if len(log) == 0:
            x = randint(1, self.n)
            y = randint(1, self.m)
            return Stone(str(x), str(y), turn)
        position = choice(self.suggest_positions(log))
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
        Stone("6", "5", "w"),
        Stone("10", "11", "b"),
        Stone("11", "11", "b"),
        Stone("6", "6", "w"),
    ]

    config = BoardConfig(19, 19, 6, 2, 1)
    tei_bot = TeiBot(config)
    tei_bot.draw_board(diagonal_test_log)

    suggest_positions = tei_bot.suggest_positions(diagonal_test_log)
    tei_bot.draw_board(suggest_positions)

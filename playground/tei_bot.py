import numpy as np
from typing import List
from board import Stone


class TeiBot:

    def __init__(self, log: List[Stone]):
        self.log = log

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

    @staticmethod
    def move_stone(stone, direction, stride=1):
        x = int(stone.x)
        y = int(stone.y)

        if direction == 'l':
            x = x - stride
        elif direction == 'r':
            x = x + stride
        elif direction == 'u':
            y = y - stride
        elif direction == 'd':
            y = y + stride
        elif direction == 'ul':
            y = y - stride
            x = x - stride
        elif direction == 'ur':
            y = y - stride
            x = x + stride
        elif direction == 'dl':
            y = y + stride
            x = x - stride
        elif direction == 'dr':
            y = y + stride
            x = x + stride

        return Stone(str(x), str(y), stone.color)

    def draw_board(self):
        stone_array = self.stone_to_array(self.log)
        join_column = list(map(lambda y: " ".join([self.array_to_board(x) for i, x in enumerate(y)]), stone_array))
        join_row = "\n" + "\n".join(join_column)
        print(join_row)

    def suggest_positions(self, lower=1, upper=19) -> List[Stone]:
        suggestions = []
        for d in ['r', 'l', 'u', 'd', 'ul', 'ur', 'dl', 'dr']:
            position = list(map(lambda x: self.move_stone(x, d, 1), self.log))
            position = list(filter(lambda x: lower <= int(x.x) <= upper and lower <= int(x.y) <= upper, position))
            suggestions = suggestions + position

        suggestions = set(map(lambda x: x.x + " " + x.y, suggestions))
        suggestions = list(map(lambda x: x.split(" "), suggestions))
        suggestions = list(map(lambda z: Stone(z[0], z[1], 's'), suggestions))
        stone_array = self.stone_to_array(self.log)
        suggestions = self.stone_to_array(suggestions)
        suggestions = np.clip(stone_array + suggestions, -1, 0)
        suggestions = self.array_to_stone(suggestions, "s")

        return suggestions


if __name__ == "__main__":
    test_log = [
        Stone("1", "1", "b"),
        Stone("2", "1", "w"),
        Stone("2", "2", "w"),
        Stone("1", "2", "b"),
        Stone("1", "3", "b"),
        Stone("2", "3", "w"),
        Stone("2", "4", "w"),
        Stone("1", "4", "b"),
        Stone("1", "5", "b"),
        Stone("2", "5", "w"),
        Stone("2", "6", "w"),
    ]
    test_horizontal_log = [
        Stone("1", "1", "b"),
        Stone("1", "2", "w"),
        Stone("2", "2", "w"),
        Stone("2", "1", "b"),
        Stone("3", "1", "b"),
        Stone("3", "2", "w"),
        Stone("4", "2", "w"),
        Stone("4", "1", "b"),
        Stone("5", "1", "b"),
        Stone("5", "2", "w"),
        Stone("15", "2", "w"),
        Stone("5", "4", "b"),
        Stone("7", "3", "b"),
        Stone("6", "2", "w")
    ]
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

    test_result = TeiBot(diagonal_test_log)
    test_result.draw_board()

    a2 = test_result.suggest_positions()
    TeiBot(a2).draw_board()

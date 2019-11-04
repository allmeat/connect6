import numpy as np
from typing import List
from board import Stone


class ReadBoard:

    def __init__(self, logs:List[Stone]):
        self.logs=logs

    @staticmethod
    def np2board(x):
        if x==0:
            out="+"
        elif x==1:
            out="B"
        elif x==2:
            out="W"
        elif x==-1:
            out="S"
        return out


    @staticmethod
    def stone2np(logs):
        aa = np.zeros((21, 21))
        for pos in logs:
            x = int(pos.x) - 1
            y = int(pos.y) - 1
            if pos.color == "b":
                aa[y, x] = 1
            elif pos.color == "w":
                aa[y, x] = 2
            elif pos.color == "s":
                aa[y, x] = -1
        return aa

    @staticmethod
    def np2stone(npArray, col):

        if col=="b":
            out=1
        elif col=="w":
            out=2
        elif col == "s":
            out=-1

        y, x = np.where(npArray==out)
        coord = list(zip(list(x), list(y)))
        stones = [Stone(str(x+1), str(y+1), col) for x, y in coord]

        return stones

    @staticmethod
    def move(stone, direction, stride=1):

        x = int(stone.x)
        y = int(stone.y)

        if direction == 'l':
            x = x - stride
        if direction == 'r':
            x = x + stride
        if direction == 'u':
            y = y - stride
        if direction == 'd':
            y = y + stride
        if direction == 'ul':
            y = y - stride
            x = x - stride
        if direction == 'ur':
            y = y - stride
            x = x + stride
        if direction == 'dl':
            y = y + stride
            x = x - stride
        if direction == 'dr':
            y = y + stride
            x = x + stride

        return Stone(str(x), str(y), stone.color)


    def drawboard(self):

        npData = self.stone2np(self.logs)
        alphabet = "a b c d e f g h i j k l m n o p q r s t u".split(" ")
        rowIndex = " ".join(list(map(lambda y : y, alphabet)))
        a1 = list(map(lambda y: " ".join([self.np2board(x) for i, x in enumerate(y)]), npData))
        a2 = rowIndex + "\n" + "\n".join(a1)
        return a2


    def suggestedPosition(self, l=1, u=21):

        suggested = []
        for d in ['r', 'l', 'u', 'd', 'ul', 'ur', 'dl', 'dr']:
            position = list(map(lambda x: self.move(x, d, 1), self.logs))
            position = list(filter(lambda x: int(x.x)>=l and int(x.x)<=u and int(x.y)>=l and int(x.y)<=u, position))
            suggested = suggested + position

        suggested = set(map(lambda x: x.x + " " + x.y, suggested))
        suggested = list(map(lambda x: x.split(" "), suggested))
        suggested = list(map(lambda z: Stone(z[0], z[1], 's'), suggested))
        npLogs = self.stone2np(self.logs)
        suggested = self.stone2np(suggested)
        suggested = np.clip(npLogs + suggested, -1, 0)
        suggested = self.np2stone(suggested, "s")

        return suggested


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

    logs = ReadBoard(diagonal_test_log)
    print(logs.drawboard())

    a2 = logs.suggestedPosition()
    print(ReadBoard(a2).drawboard())


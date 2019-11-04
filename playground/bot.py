from typing import List
from random import randint
from board import Stone
from tei_bot import ReadBoard
from random import choice

class Bot:

    def __init__(self, color: str):
        self.color = color

    def random_bot(self) -> Stone:
        x = randint(1, 19)
        y = randint(1, 19)
        return Stone(str(x), str(y), self.color)

    def linear_bot(self, log: List[Stone]) -> Stone:
        return Stone(str(10), str(10), self.color)

    def tei_bot(self, log: List[Stone]) -> Stone:
        possible_pos = ReadBoard(log).suggestedPosition()
        pos = choice(possible_pos)
        pos.color = self.color
        return pos

if __name__ == "__main__":
    bot = Bot("w")
    print("--random bot")
    print("\t--white random stone: ", bot.random_bot())

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


    print(ReadBoard(diagonal_test_log).suggestedPosition())
    print(bot.tei_bot(diagonal_test_log))

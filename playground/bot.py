from typing import List
from random import randint
from board import Stone
from tei_bot import TeiBot
from alex_bot import AlexBot


class Bot:

    def __init__(self):
        self.tei = TeiBot()
        self.alex = AlexBot()

    @staticmethod
    def turn_check(log_length: int) -> str:
        return "b" if (log_length + 1) % 4 in [0, 1] else "w"

    @staticmethod
    def random_bot(color: str) -> Stone:
        x = randint(1, 19)
        y = randint(1, 19)
        return Stone(str(x), str(y), color)

    def tei_bot(self, log: List[Stone]) -> Stone:
        return self.tei.put_stone(log)

    def alex_bot(self, log: List[Stone]) -> Stone:
        return self.alex.put_stone(log)


if __name__ == "__main__":
    bot = Bot()
    test_log = [
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
    ]

    print("--random bot")
    print("\t--white random stone: ", bot.random_bot("w"))

    print("--Tei bot")
    print("\t--white Tei bot stone: ", bot.tei_bot(test_log))

    print("--Alex bot")
    print("\t--white Alex bot stone: ", bot.alex_bot(test_log))

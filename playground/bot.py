from typing import List
from random import randint
from board import Stone, BoardConfig
from tei_bot import TeiBot
from alex_bot import AlexBot


class Bot:

    def __init__(self, board_config: BoardConfig):
        self.config = board_config
        self.tei = TeiBot(self.config)
        self.alex = AlexBot(self.config)

    def random_bot(self, color: str) -> Stone:
        x = randint(1, self.config.column)
        y = randint(1, self.config.row)
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

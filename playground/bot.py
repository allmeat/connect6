from random import randint
from typing import List

from board import Stone
from strategic_bot import get_scheme


class Bot:

    def __init__(self, color: str):
        self.color = color

    def random_bot(self) -> Stone:
        x = randint(1, 19)
        y = randint(1, 19)
        return Stone(str(x), str(y), self.color)

    def linear_bot(self, log: List[Stone]) -> Stone:
        return Stone(str(10), str(10), self.color)

    def strategic_bot(self, log: List[Stone]) -> Stone:
        return get_scheme(self.color, log)


if __name__ == "__main__":
    bot = Bot("w")
    print("--random bot")
    print("\t--white random stone: ", bot.random_bot())

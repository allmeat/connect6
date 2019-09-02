from typing import List
from random import randint
from playground.board import Stone


class Bot:

    def __init__(self, color: str):
        self.color = color

    def random_bot(self) -> Stone:
        x = randint(1, 19)
        y = randint(1, 19)
        return Stone(str(x), str(y), self.color)

    def linear_bot(self, log: List[Stone]) -> Stone:
        return Stone(str(10), str(10), self.color)


if __name__ == "__main__":
    bot = Bot("w")
    print("--random bot")
    print("\t--white random stone: ", bot.random_bot())

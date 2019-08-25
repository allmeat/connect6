from random import randint
from board import Stone


class Bot:

    def __init__(self, color: str):
        self.color = color

    def random_bot(self) -> Stone:
        x = randint(1, 19)
        y = randint(1, 19)
        return Stone(str(x), str(y), self.color)


if __name__ == "__main__":
    bot = Bot("w")
    print("--random bot")
    print("\t--white random stone: ", bot.random_bot())

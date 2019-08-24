from random import randint
from server import Stone


class Bot:

    @staticmethod
    def random_bot(stone: str):
        x = randint(1, 19)
        y = randint(1, 19)
        return Stone(x, y, stone)


if __name__ == "__main__":
    bot = Bot()
    print(bot.random_bot("w"))

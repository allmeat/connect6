from random import randint
from server import Stone


def random_bot(stone: str):
    x = randint(1, 19)
    y = randint(1, 19)
    return Stone(x, y, stone)


if __name__ == "__main__":
    print(random_bot("w"))

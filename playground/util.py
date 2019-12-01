from typing import List
from board import Stone


def turn_check(log: List[Stone], each_move: int, first_move: int) -> str:
    if (len(log) - first_move) % (2 * each_move) in list(range(0, each_move)):
        return "w"
    return "b"

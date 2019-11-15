import numpy as np
from random import choice
from dataclasses import dataclass
from typing import List, Tuple
from board import Stone


@dataclass
class Window:
    pattern: List[int]
    position: List[Tuple[int, int]]


class Bot:

    def __init__(self, k: int = 6, m: int = 19, n: int = 19):
        self.k = k
        self.m = m
        self.n = n

    def alex_bot(self, log: List[Stone]) -> Stone:
        turn = "b" if (len(log) + 1) % 4 in [0, 1] else "w"
        if len(log) == 0:
            return Stone(str(10), str(10), turn)

        if len(log) == 1:
            next_x = int(log[0].x) + choice([-1, 1])
            next_y = int(log[0].y) + choice([-1, 1])
            return Stone(str(next_x), str(next_y), turn)

        log_x = [int(stone.x) for stone in log]
        log_y = [int(stone.y) for stone in log]

        left_end = max(min(log_x) - self.k, 1)
        right_end = min(max(log_x) + self.k, self.m)
        upper_end = max(min(log_y) - self.k, 1)
        lower_end = min(max(log_y) + self.k, self.n)

        focus_area = np.zeros((lower_end - upper_end, right_end - left_end), dtype=int)
        for stone in log:
            focus_area[int(stone.y) - upper_end, int(stone.x) - left_end] = 1 if stone.color == "b" else -1

        horizontal = self.find_connection(focus_area, "h", left_end, upper_end)
        vertical = self.find_connection(focus_area, "v", left_end, upper_end)
        negative_diagonal = self.find_connection(focus_area, "nd", left_end, upper_end)
        positive_diagonal = self.find_connection(focus_area, "pd", left_end, upper_end)

        candidates = (
            sorted(
                horizontal + vertical + negative_diagonal + positive_diagonal,
                key=lambda x: abs(sum(x.pattern)),
                reverse=True,
            )
        )

        window_index = choice([i for i, x in enumerate(candidates[0].pattern) if x == 0])
        position = candidates[0].position[window_index]

        return Stone(str(position[0]), str(position[1]), turn)

    def find_connection(self,
                        focus_area: np.ndarray,
                        direction: str,
                        left_end: int,
                        upper_end: int,
                        ) -> List[Window]:
        connections = []
        max_stone = 0

        if direction == "h" or direction == "horizontal":
            for row in range(focus_area.shape[0]):
                for column in range(focus_area.shape[1]):
                    window = (
                        Window(
                            pattern=focus_area[row, column:(column + self.k)],
                            position=[(row + upper_end, column + left_end + i) for i in range(self.k)],
                        )
                    )
                    connections, max_stone = self.check_window(window, connections, max_stone)
            return connections

        if direction == "v" or direction == "vertical":
            for column in range(focus_area.shape[1]):
                for row in range(focus_area.shape[0]):
                    window = (
                        Window(
                            pattern=focus_area[row:(row + self.k), column],
                            position=[(row + upper_end + i, column + left_end) for i in range(self.k)],
                        )
                    )
                    connections, max_stone = self.check_window(window, connections, max_stone)
            return connections

        if direction == "nd" or direction == "negative_diagonal":
            for row in range(focus_area.shape[0] - self.k + 1):
                for column in range(focus_area.shape[1] - self.k + 1):
                    window = (
                        Window(
                            pattern=focus_area[row:(row + self.k), column:(column + self.k)].diagonal(),
                            position=[(row + upper_end + i, column + left_end + i) for i in range(self.k)],
                        )
                    )
                    connections, max_stone = self.check_window(window, connections, max_stone)
            return connections

        if direction == "pd" or direction == "positive_diagonal":
            for row in range(focus_area.shape[0] - self.k + 1):
                for column in range(focus_area.shape[1] - self.k + 1):
                    window = (
                        Window(
                            pattern=np.fliplr(focus_area[row:(row + self.k), column:(column + self.k)]).diagonal(),
                            position=[(row + upper_end + i, column + left_end + self.k - 1 - i) for i in range(self.k)],
                        )
                    )
                    connections, max_stone = self.check_window(window, connections, max_stone)
            return connections

    @staticmethod
    def check_window(window: Window,
                     connections: List[Window],
                     max_stone: int,
                     ) -> (List[Window], int):
        if 1 in window.pattern and -1 in window.pattern:
            return connections, max_stone

        stone_count = abs(sum(window.pattern))

        if max_stone > stone_count:
            return connections, max_stone

        if max_stone < stone_count:
            return [window], stone_count

        connections.append(window)
        return connections, max_stone


if __name__ == "__main__":
    test_log = [
        Stone("3", "2", "b"),
        Stone("2", "1", "w"),
        Stone("2", "2", "w"),
        Stone("1", "2", "b"),
        Stone("1", "3", "b"),
        Stone("2", "3", "w"),
        Stone("2", "4", "w"),
        Stone("1", "4", "b"),
        Stone("1", "5", "b"),
        Stone("2", "5", "w"),
        Stone("2", "8", "w"),
        Stone("1", "10", "b"),
        Stone("1", "11", "b"),
        Stone("2", "9", "w"),
        Stone("2", "6", "w"),
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
        Stone("8", "4", "w"),
        Stone("7", "10", "b"),
        Stone("8", "10", "b"),
        Stone("9", "11", "w"),
        Stone("6", "7", "w"),
        Stone("4", "10", "b"),
        Stone("5", "10", "b"),
        Stone("7", "5", "w"),
    ]
    bot = Bot()
    # print("\t--basic bot: ", bot.alex_bot(test_log))
    print("\t--basic bot: ", bot.alex_bot(diagonal_test_log))

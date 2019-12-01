import numpy as np
from random import choice
from dataclasses import dataclass
from typing import List, Tuple
from board import Stone


@dataclass
class Window:
    pattern: List[int]
    position: List[Tuple[int, int]]


class AlexBot:

    def __init__(self, k: int = 6, m: int = 19, n: int = 19):
        self.k = k  # number of stones in a row for winning
        self.m = m  # number of row on board
        self.n = n  # number of column on board

    def put_stone(self, log: List[Stone]) -> Stone:
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

        width = right_end - left_end + 1
        height = lower_end - upper_end + 1

        focus_area = np.zeros((height, width), dtype=int)
        for stone in log:
            normalize_row_index = int(stone.y) - upper_end
            normalize_column_index = int(stone.x) - left_end
            focus_area[normalize_row_index, normalize_column_index] = 1 if stone.color == "b" else -1

        horizontal = self.find_connection(focus_area, "h", left_end, upper_end)
        vertical = self.find_connection(focus_area, "v", left_end, upper_end)
        negative_diagonal = self.find_connection(focus_area, "nd", left_end, upper_end)
        positive_diagonal = self.find_connection(focus_area, "pd", left_end, upper_end)
        candidates = horizontal + vertical + negative_diagonal + positive_diagonal
        if len(candidates) == 0:
            print("expect tie")
            random_empty_spot = choice(self.empty_spots(log))
            return Stone(random_empty_spot.x, random_empty_spot.y, turn)

        max_stone = max([self.stone_sum(candidate) for candidate in candidates])
        if max_stone >= self.k:
            return Stone("1", "1", turn)
        max_stone_candidates = [candidate for candidate in candidates if self.stone_sum(candidate) == max_stone]
        max_stone_candidate = choice(max_stone_candidates)
        window_index = (
            sorted(
                [i for i, x in enumerate(max_stone_candidate.pattern) if x == 0],
                key=lambda x: abs(x - self.k / 2),
            )[0]
        )
        position = max_stone_candidate.position[window_index]

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
                for column in range(focus_area.shape[1] - self.k + 1):
                    window = (
                        Window(
                            pattern=focus_area[row, column:(column + self.k)],
                            position=[(column + left_end + i, row + upper_end) for i in range(self.k)],
                        )
                    )
                    connections, max_stone = self.check_window(window, connections, max_stone)
            return connections

        if direction == "v" or direction == "vertical":
            for column in range(focus_area.shape[1]):
                for row in range(focus_area.shape[0] - self.k + 1):
                    window = (
                        Window(
                            pattern=focus_area[row:(row + self.k), column],
                            position=[(column + left_end, row + upper_end + i) for i in range(self.k)],
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
                            position=[(column + left_end + i, row + upper_end + i) for i in range(self.k)],
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
                            position=[(column + left_end + self.k - 1 - i, row + upper_end + i) for i in range(self.k)],
                        )
                    )
                    connections, max_stone = self.check_window(window, connections, max_stone)
            return connections

    def check_window(self,
                     window: Window,
                     connections: List[Window],
                     max_stone: int,
                     ) -> (List[Window], int):
        if 1 in window.pattern and -1 in window.pattern:
            return connections, max_stone

        stone_count = self.stone_sum(window)

        if max_stone > stone_count:
            return connections, max_stone

        if max_stone < stone_count:
            return [window], stone_count

        connections.append(window)
        return connections, max_stone

    @staticmethod
    def stone_sum(window: Window) -> int:
        return abs(sum(window.pattern))

    def empty_spots(self, log: List[Stone]) -> List[Stone]:
        full_area = np.zeros((self.n, self.m), dtype=int)
        for item in log:
            full_area[int(item.y) - 1, int(item.x) - 1] = 1
        empty_spot_index = np.where(full_area == 0)
        empty_spot_list = []
        for coordinate in list(zip(empty_spot_index[0], empty_spot_index[1])):
            empty_spot_list.append(Stone(str(coordinate[1] + 1), str(coordinate[0] + 1), "empty"))
        return empty_spot_list


if __name__ == "__main__":
    vertical_test_log = [
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
        Stone("1", "8", "b"),
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

    alex_bot = AlexBot()
    print("--Alex bot")
    print("\t--x = 2, y = 6, color = w (vertical test): ", alex_bot.put_stone(vertical_test_log))
    print("\t--x = 6, y = 6, color = w (diagonal test): ", alex_bot.put_stone(diagonal_test_log))

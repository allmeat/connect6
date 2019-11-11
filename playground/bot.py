import numpy as np
from dataclasses import dataclass
from typing import List
from random import randint, random
from board import Stone

@dataclass
class Connection:
    length: int
    is_open: bool


class Bot:

    def __init__(self, color: str):
        self.color = color

    def random_bot(self) -> Stone:
        x = randint(1, 19)
        y = randint(1, 19)
        return Stone(str(x), str(y), self.color)

    @staticmethod
    def check_turn(log: List[Stone]) -> str:
        return "b" if (len(log) + 1) % 4 in [0, 1] else "w"

    @staticmethod
    def random_walk() -> int:
        return 1 if random() > 0.5 else -1

    @staticmethod
    def color_to_int(color: str) -> int:
        return 1 if color == "b" else -1

    def alex_bot(self, log: List[Stone], k: int = 6) -> Stone:
        turn = self.check_turn(log)
        if len(log) == 0:
            return Stone(str(10), str(10), turn)

        if len(log) == 1:
            next_x = int(log[0].x) + self.random_walk()
            next_y = int(log[0].y) + self.random_walk()
            return Stone(str(next_x), str(next_y), turn)

        log_x = [int(stone.x) for stone in log]
        log_y = [int(stone.y) for stone in log]

        left_edge = max(min(log_x) - k, 1)
        right_edge = min(max(log_x) + k, 19)
        upper_edge = max(min(log_y) - k, 1)
        lower_edge = min(max(log_y) + k, 19)
        # print(left_edge)
        # print(right_edge)
        # print(upper_edge)
        # print(lower_edge)

        field = np.zeros((lower_edge - upper_edge + 1, right_edge - left_edge + 1, ), dtype=int)
        for stone in log:
            field[int(stone.y) - upper_edge, int(stone.x) - left_edge] = self.color_to_int(stone.color)

        horizontal = []
        for i in range(field.shape[0]):
            for j in range(right_edge - k + 1):
                window = field[i, j:(j + k)]
                if not (1 in window and -1 in window) and abs(sum(window)) > 0:
                    horizontal.append(Connection(abs(sum(window)), True))

        vertical = []
        for i in range(field.shape[1]):
            for j in range(lower_edge - k + 1):
                window = field[j:(j + k), i]
                if not (1 in window and -1 in window) and abs(sum(window)) > 0:
                    vertical.append(Connection(abs(sum(window)), True))

        positive_diagonal = []

        print(field)
        print(horizontal)
        print(vertical)

        return Stone(str(10), str(10), turn)

        # @staticmethod
        # def cartesian_connection_check(groups: DefaultDict[int, List]) -> List[List[(int, int)]]:
        #     for group_key in groups:
        #         group = groups[group_key]
        #         sort_group = sorted(group)
        #         diff = [str(sort_group[i + 1] - sort_group[i]) for i in range(len(sort_group) - 1)]
        #         diff_string = [len(d) for d in "".join(diff).split("0") if len(d) > 0]

        # @staticmethod
        # def diagonal_connection_check(current_position: List[int], all_position: List[List[int]]) -> int:
        #     recursive
        # def count_lower_right(cnt: int, current: List[int]) -> int:
        #     next_position = [p + 1 for p in current]
        #     if next_position in all_position:
        #         cnt = count_lower_right(cnt + 1, next_position)
        #         return cnt
        #     else:
        #         return cnt
        #
        # return count_lower_right(0, current_position)

        # @staticmethod
        # def reverse_stone_color(color: str) -> str:
        #     return "b" if color == "w" else "w"
        #
        # def sort_line(self, line: List[StoneOnLine], turn: str) -> List[StoneOnLine]:
        #     line = sorted(line, key=lambda stone_on_line: stone_on_line.position)
        #     if line[0].position == 1:
        #         line.insert(0, StoneOnLine(0, self.reverse_stone_color(turn)))
        #     if line[-1].position == 19:
        #         line.append(StoneOnLine(20, self.reverse_stone_color(turn)))
        #     return line

        # horizontal = [StoneOnLine(int(stone.x), stone.color) for stone in log if stone.y == str(y)]
        # horizontal = self.sort_line(horizontal, turn)

        # vertical search
        # for x in range(min(log_x), max(log_x)):
        #     vertical = [StoneOnLine(int(stone.y), stone.color) for stone in log if stone.x == str(x)]
        #     vertical = self.sort_line(vertical, turn)

        # log_dict = defaultdict(list)
        # for item in log:
        #     log_dict[item.color].append((int(item.x), int(item.y)))
        # black_stones = log_dict["b"]
        # white_stones = log_dict["w"]

        # log_dict = self.list_to_dict(log)
        # longest_open_connection =
        # longes_half_open_connection =
        # focus_latest = self.limit_focus(log[-1])
        # for candidates in focus_latest:
        #     stone_color = []
        #     for candidate in candidates:
        #         stone_color.append(log_dict.get(candidate, ""))
        #     print(stone_color)

        # result =


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
        # Stone("17", "17", "b"),
        # Stone("18", "18", "b"),
    ]
    bot = Bot("w")
    print("--random bot")
    print("\t--white random stone: ", bot.random_bot())
    print("\t--basic bot: ", bot.alex_bot(test_log))

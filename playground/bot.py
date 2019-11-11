from typing import List, DefaultDict
from collections import defaultdict
from dataclasses import dataclass
from random import randint, random
from board import Stone


@dataclass
class StoneOnLine:
    position: int
    color: str


class Bot:

    def __init__(self, color: str):
        self.color = color

    def random_bot(self) -> Stone:
        x = randint(1, 19)
        y = randint(1, 19)
        return Stone(str(x), str(y), self.color)

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

    @staticmethod
    def check_turn(log: List[Stone]) -> str:
        return "b" if (len(log) + 1) % 4 in [0, 1] else "w"

    @staticmethod
    def random_walk() -> int:
        return 1 if random() > 0.5 else -1

    @staticmethod
    def reverse_stone_color(color: str) -> str:
        return "b" if color == "w" else "w"

    def sort_line(self, line: List[StoneOnLine], turn: str) -> List[StoneOnLine]:
        line = sorted(line, key=lambda stone_on_line: stone_on_line.position)
        if line[0].position == 1:
            line.insert(0, StoneOnLine(0, self.reverse_stone_color(turn)))
        if line[-1].position == 19:
            line.append(StoneOnLine(20, self.reverse_stone_color(turn)))
        return line

    def alex_bot(self, log: List[Stone]) -> Stone:
        turn = self.check_turn(log)
        if len(log) == 0:
            result = Stone(str(10), str(10), turn)
        elif len(log) == 1:
            next_x = int(log[0].x) + self.random_walk()
            next_y = int(log[0].y) + self.random_walk()
            result = Stone(str(next_x), str(next_y), turn)
        else:
            log_x = [int(stone.x) for stone in log]
            log_y = [int(stone.y) for stone in log]

            # horizontal search
            for y in range(min(log_y), max(log_y)):
                horizontal = [StoneOnLine(int(stone.x), stone.color) for stone in log if stone.y == str(y)]
                horizontal = self.sort_line(horizontal, turn)

            # vertical search
            for x in range(min(log_x), max(log_x)):
                vertical = [StoneOnLine(int(stone.y), stone.color) for stone in log if stone.x == str(x)]
                vertical = self.sort_line(vertical, turn)


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

            result = Stone(str(10), str(10), turn)

        return result


if __name__ == "__main__":
    test_log = [
        Stone("1", "1", "b"),
        Stone("2", "1", "w"),
        Stone("2", "2", "w"),
        Stone("1", "2", "b"),
        Stone("1", "3", "b"),
        Stone("2", "3", "w"),
        Stone("2", "4", "w"),
        Stone("1", "4", "b"),
        Stone("1", "5", "b"),
        Stone("2", "5", "w"),
        # Stone("2", "8", "w"),
        # Stone("1", "10", "b"),
        # Stone("1", "11", "b"),
        # Stone("2", "9", "w"),
        # Stone("2", "6", "w"),
    ]
    bot = Bot("w")
    print("--random bot")
    print("\t--white random stone: ", bot.random_bot())
    # print("\t--basic bot: ", bot.basic_bot(test_log))

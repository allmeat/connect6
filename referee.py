from typing import List, DefaultDict
from board import Stone
from collections import defaultdict


class Referee:

    @staticmethod
    def valid_check(new_stone: Stone, log: List[Stone]) -> bool:
        x_valid_range = (int(new_stone.x) > 0) & (int(new_stone.x) < 20)
        y_valid_range = (int(new_stone.y) > 0) & (int(new_stone.y) < 20)
        coordinate = [[stone.x, stone.y] for stone in log]
        empty_seat = [new_stone.x, new_stone.y] not in coordinate
        return x_valid_range & y_valid_range & empty_seat

    @staticmethod
    def turn_check(log: List[Stone]) -> str:
        if (len(log) + 1) % 4 in [0, 1]:
            return "b"
        else:
            return "w"

    def end_check(self, log: List[Stone]) -> str:
        log_dict = defaultdict(list)
        for item in log:
            log_dict[item.color].append([int(item.x), int(item.y)])
        black_stones = log_dict["b"]
        white_stones = log_dict["w"]

        black_wins = self.connection_check(black_stones)
        white_wins = self.connection_check(white_stones)

        if black_wins:
            return "black wins"
        elif white_wins:
            return "white wins"
        else:
            return "keep play"

    def connection_check(self, positions: List[List[int]]) -> bool:
        horizontal_dict = defaultdict(list)
        vertical_dict = defaultdict(list)
        diagonal_count = [0]
        for p in positions:
            horizontal_dict[p[0]].append(p[1])
            vertical_dict[p[1]].append(p[0])
            diagonal_count.append(self.diagonal_connection_check(p, positions))

        horizontal_check = self.cartesian_connection_check(horizontal_dict)
        vertical_check = self.cartesian_connection_check(vertical_dict)
        diagonal_check = max(diagonal_count) >= 5

        return horizontal_check | vertical_check | diagonal_check

    @staticmethod
    def cartesian_connection_check(groups: DefaultDict[int, List]) -> bool:
        if len(groups) == 0:
            return False
        else:
            for group_key in groups:
                group = groups[group_key]
                if len(group) >= 6:
                    sort_group = sorted(group)
                    diff = [str(sort_group[i + 1] - sort_group[i]) for i in range(len(sort_group) - 1)]
                    diff_string = ",".join(diff)
                    if "1,1,1,1,1" in diff_string:
                        return True
                    else:
                        return False
                else:
                    return False

    @staticmethod
    def diagonal_connection_check(current_position: List[int], all_position: List[List[int]]) -> int:
        # recursive
        def count_lower_right(cnt: int, current: List[int]) -> int:
            next_position = [p + 1 for p in current]
            if next_position in all_position:
                cnt = count_lower_right(cnt + 1, next_position)
                return cnt
            else:
                return cnt
        return count_lower_right(0, current_position)


if __name__ == "__main__":
    referee = Referee()
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
        Stone("6", "5", "w"),
        Stone("10", "11", "b"),
        Stone("11", "11", "b"),
        Stone("6", "6", "w"),
    ]
    print("--valid_check")
    print("\t--valid stone: ", referee.valid_check(Stone("10", "10", "b"), test_log))
    print("\t--invalid stone:", referee.valid_check(Stone("1", "1", "w"), test_log))
    print("--turn_check")
    print("\t--white turn: ", referee.turn_check(test_log[:-1]))
    print("\t--black turn: ", referee.turn_check(test_log))
    print("--end_check")
    print("\t--keep play: ", referee.end_check(test_log[:-1]))
    print("\t--white wins (horizontal): ", referee.end_check(test_log))
    print("\t--white wins (diagonal): ", referee.end_check(diagonal_test_log))
